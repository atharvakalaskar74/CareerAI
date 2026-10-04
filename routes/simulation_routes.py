import copy
from flask import Blueprint, render_template, request, jsonify, g, flash, redirect, url_for
from models.assessment import Assessment, Prediction
from models.profile import StudentSkill, Skill
from services.assessment_service import extract_ml_feature_vector
from ml.predict import get_career_predictor
from routes.auth_routes import login_required

simulation_bp = Blueprint("simulation", __name__)

@simulation_bp.route("/simulator")
@login_required
def simulator():
    # Fetch student's latest assessment or default baseline
    latest = Assessment.query.filter_by(user_id=g.user.id).order_by(Assessment.created_at.desc()).first()
    
    if latest:
        raw_responses = latest.get_raw_responses()
        baseline_vector = extract_ml_feature_vector(raw_responses)
    else:
        # Default baseline if student hasn't taken assessment
        baseline_vector = {
            "python": 6.0, "java": 5.0, "c": 4.0, "cpp": 4.0, "javascript": 5.0,
            "sql": 6.0, "html_css": 5.0, "machine_learning": 5.0, "deep_learning": 3.0,
            "data_analysis": 6.0, "cloud": 4.0, "cybersecurity": 4.0, "networking": 4.0,
            "database": 5.0, "git_github": 6.0, "problem_solving": 6.0,
            "analytical_thinking": 6.0, "communication": 6.0, "math_level": 6.0,
            "stats_level": 6.0, "cgpa": 7.5
        }

    # Run genuine ML inference on baseline
    predictor = get_career_predictor()
    if not predictor.is_ready():
        predictor._load_artifacts()
        
    baseline_pred = predictor.predict_career(baseline_vector, top_n=5)

    return render_template(
        "simulation/what_if.html",
        baseline_vector=baseline_vector,
        baseline_pred=baseline_pred
    )

@simulation_bp.route("/api/simulate", methods=["POST"])
@login_required
def api_simulate():
    """
    Reruns the actual trained ML model on modified simulation feature vectors.
    Computes genuine BEFORE vs AFTER probability shifts.
    """
    data = request.get_json() or {}
    baseline_vector = data.get("baseline", {})
    simulated_vector = data.get("simulated", {})

    if not baseline_vector or not simulated_vector:
        return jsonify({"status": "error", "message": "Missing baseline or simulated feature vectors."}), 400

    predictor = get_career_predictor()
    if not predictor.is_ready():
        predictor._load_artifacts()

    # Predict BEFORE (Baseline)
    before_result = predictor.predict_career(baseline_vector, top_n=5)
    
    # Predict AFTER (Simulated)
    after_result = predictor.predict_career(simulated_vector, top_n=5)

    # Compute differential shifts
    before_map = {item["career_title"]: item["compatibility_score"] for item in before_result["all_predictions"]}
    
    shifts = []
    for item in after_result["top_predictions"]:
        career = item["career_title"]
        after_score = item["compatibility_score"]
        before_score = before_map.get(career, 0.0)
        diff = round(after_score - before_score, 1)
        shifts.append({
            "career_title": career,
            "before_score": before_score,
            "after_score": after_score,
            "shift": diff,
            "direction": "up" if diff > 0 else ("down" if diff < 0 else "neutral")
        })

    return jsonify({
        "status": "success",
        "before": before_result,
        "after": after_result,
        "shifts": shifts
    })
