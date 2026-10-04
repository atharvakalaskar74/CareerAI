import json
import logging
from database.db import db
from models.user import User
from models.profile import StudentProfile, Skill, StudentSkill
from models.career import Career
from models.assessment import (
    Assessment, Prediction, PredictionExplanation,
    SkillGap, Roadmap, RoadmapItem, ProgressRecord
)
from services.scoring_service import calculate_profile_scores
from services.skill_gap_service import calculate_skill_gaps_for_career
from services.roadmap_service import generate_personalized_roadmap
from ml.predict import get_career_predictor
from ml.explain import explain_prediction

logger = logging.getLogger(__name__)

def extract_ml_feature_vector(raw_responses):
    """
    Extracts the exact 21 features required by the ML model
    from the multi-section assessment questionnaire.
    """
    academic = raw_responses.get("academic", {})
    tech = raw_responses.get("technical_skills", {})
    soft = raw_responses.get("soft_skills", {})

    return {
        "python": float(tech.get("python", 5.0)),
        "java": float(tech.get("java", 5.0)),
        "c": float(tech.get("c", 4.0)),
        "cpp": float(tech.get("cpp", 4.0)),
        "javascript": float(tech.get("javascript", 5.0)),
        "sql": float(tech.get("sql", 5.0)),
        "html_css": float(tech.get("html_css", 5.0)),
        "machine_learning": float(tech.get("machine_learning", 4.0)),
        "deep_learning": float(tech.get("deep_learning", 3.0)),
        "data_analysis": float(tech.get("data_analysis", 5.0)),
        "cloud": float(tech.get("cloud", 4.0)),
        "cybersecurity": float(tech.get("cybersecurity", 4.0)),
        "networking": float(tech.get("networking", 4.0)),
        "database": float(tech.get("database", 5.0)),
        "git_github": float(tech.get("git_github", 5.0)),
        "problem_solving": float(soft.get("problem_solving", 6.0)),
        "analytical_thinking": float(soft.get("analytical_thinking", 6.0)),
        "communication": float(soft.get("communication", 6.0)),
        "math_level": float(academic.get("math_level", 6.0)),
        "stats_level": float(academic.get("stats_level", 6.0)),
        "cgpa": float(academic.get("cgpa", 7.5))
    }

def process_student_assessment(user_id, raw_responses):
    """
    Coordinates the full end-to-end processing of a student assessment:
    1. Computes profile scores (Technical, Readiness, Academic, Problem Solving, Soft, Practical).
    2. Runs genuine ML prediction pipeline on student feature vector.
    3. Generates Explainable AI (XAI) feature attribution.
    4. Computes Skill Gap analysis for recommended top career.
    5. Builds personalized 6-phase learning roadmap.
    6. Persists everything in relational database tables.
    """
    # 1. Indicator scores
    profile_scores = calculate_profile_scores(raw_responses)
    
    # 2. ML feature vector
    feature_vector = extract_ml_feature_vector(raw_responses)
    
    # 3. Real ML Model Prediction
    predictor = get_career_predictor()
    if not predictor.is_ready():
        # Fallback if model not loaded
        from ml.train import train_and_evaluate_models
        train_and_evaluate_models()
        predictor._load_artifacts()

    pred_result = predictor.predict_career(feature_vector, top_n=5)
    top_career_title = pred_result["top_career"]
    top_compatibility = pred_result["top_compatibility"]
    confidence_score = pred_result["confidence_score"]

    # Match top career title to database Career record
    top_career = Career.query.filter_by(title=top_career_title).first()
    if not top_career:
        top_career = Career.query.first()

    # 4. Explainable AI (XAI)
    explanation = explain_prediction(
        predictor.model,
        predictor.preprocessor,
        feature_vector,
        top_career_title,
        top_compatibility
    )

    # 5. Skill Gap Analysis
    all_skills_combined = {**raw_responses.get("technical_skills", {}), **raw_responses.get("soft_skills", {})}
    gap_result = calculate_skill_gaps_for_career(top_career.id, all_skills_combined)

    # 6. Personalized Roadmap
    roadmap_data = generate_personalized_roadmap(top_career.id, all_skills_combined, raw_responses.get("experience", {}))

    # 7. Save to Database
    assessment = Assessment(
        user_id=user_id,
        academic_foundation_score=profile_scores["academic_foundation_score"],
        technical_score=profile_scores["technical_score"],
        soft_skill_score=profile_scores["soft_skill_score"],
        problem_solving_score=profile_scores["problem_solving_score"],
        practical_experience_score=profile_scores["practical_experience_score"],
        career_readiness_score=profile_scores["career_readiness_score"],
        raw_responses_json=json.dumps(raw_responses)
    )
    db.session.add(assessment)
    db.session.flush()

    prediction_record = Prediction(
        assessment_id=assessment.id,
        user_id=user_id,
        top_career_id=top_career.id,
        top_career_code=top_career.code,
        compatibility_score=top_compatibility,
        confidence_score=confidence_score,
        top_predictions_json=json.dumps(pred_result["top_predictions"]),
        model_version="v1.0.0"
    )
    db.session.add(prediction_record)
    db.session.flush()

    explanation_record = PredictionExplanation(
        prediction_id=prediction_record.id,
        top_positive_features_json=json.dumps(explanation["positive_features"]),
        top_negative_features_json=json.dumps(explanation["negative_features"]),
        feature_importances_json=json.dumps(explanation["all_contributions"]),
        human_readable_summary=explanation["human_readable_summary"]
    )
    db.session.add(explanation_record)

    skill_gap_record = SkillGap(
        user_id=user_id,
        career_id=top_career.id,
        assessment_id=assessment.id,
        matched_skills_json=json.dumps(gap_result["matched_skills"]),
        weak_skills_json=json.dumps(gap_result["weak_skills"]),
        missing_skills_json=json.dumps(gap_result["missing_skills"]),
        gap_score=gap_result["gap_score"]
    )
    db.session.add(skill_gap_record)

    roadmap_record = Roadmap(
        user_id=user_id,
        career_id=top_career.id,
        target_completion_months=roadmap_data["total_months"]
    )
    db.session.add(roadmap_record)
    db.session.flush()

    for item in roadmap_data["phases"]:
        r_item = RoadmapItem(
            roadmap_id=roadmap_record.id,
            phase_number=item["phase_number"],
            phase_name=item["phase_name"],
            title=item["title"],
            description=item["description"],
            skills_targeted_json=json.dumps(item["skills_targeted"]),
            resources_json=json.dumps(item["resources"]),
            estimated_weeks=item["estimated_weeks"],
            order_index=item["phase_number"]
        )
        db.session.add(r_item)

    # Progress record
    progress = ProgressRecord(
        user_id=user_id,
        assessment_id=assessment.id,
        career_readiness_score=profile_scores["career_readiness_score"],
        top_career_title=top_career_title,
        top_compatibility=top_compatibility
    )
    db.session.add(progress)

    # Update Student Profile if exists
    profile = StudentProfile.query.filter_by(user_id=user_id).first()
    academic_info = raw_responses.get("academic", {})
    work_prefs = raw_responses.get("work_preferences", {})
    
    if profile:
        profile.cgpa = float(academic_info.get("cgpa", profile.cgpa or 7.0))
        profile.math_level = int(academic_info.get("math_level", profile.math_level or 5))
        profile.stats_level = int(academic_info.get("stats_level", profile.stats_level or 5))
        profile.work_preference_style = work_prefs.get("style", profile.work_preference_style)
        profile.work_environment = work_prefs.get("environment", profile.work_environment)

    # Update or insert student skills
    for skill_name, rating in raw_responses.get("technical_skills", {}).items():
        sk_obj = Skill.query.filter(Skill.name.ilike(skill_name.replace("_", " "))).first()
        if sk_obj:
            st_skill = StudentSkill.query.filter_by(user_id=user_id, skill_id=sk_obj.id).first()
            if not st_skill:
                st_skill = StudentSkill(user_id=user_id, skill_id=sk_obj.id, proficiency_level=int(float(rating)))
                db.session.add(st_skill)
            else:
                st_skill.proficiency_level = int(float(rating))

    db.session.commit()

    return {
        "assessment_id": assessment.id,
        "prediction_id": prediction_record.id,
        "profile_scores": profile_scores,
        "prediction": pred_result,
        "explanation": explanation,
        "skill_gaps": gap_result,
        "roadmap": roadmap_data
    }
