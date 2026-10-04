import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, g
from database.db import db
from models.user import User
from models.profile import Skill, StudentProfile
from models.career import Career
from models.assessment import Assessment, Prediction, PredictionExplanation, SkillGap, Roadmap
from services.assessment_service import process_student_assessment
from routes.auth_routes import login_required

assessment_bp = Blueprint("assessment", __name__)

@assessment_bp.route("/assessment")
@login_required
def wizard():
    profile = g.user.profile
    skills = Skill.query.all()
    careers = Career.query.filter_by(is_active=1).all()
    return render_template("assessment/wizard.html", profile=profile, skills=skills, careers=careers)

def safe_int(val, default=1):
    try:
        return int(float(str(val).strip()))
    except (ValueError, TypeError):
        return default

def safe_float(val, default=5.0):
    try:
        return float(str(val).strip())
    except (ValueError, TypeError):
        return default

@assessment_bp.route("/assessment/submit", methods=["POST"])
@login_required
def submit_assessment():
    try:
        if request.is_json:
            raw_data = request.get_json()
        else:
            # Parse form fields
            form = request.form
            raw_data = {
                "academic": {
                    "qualification": form.get("highest_qualification", "12th / High School"),
                    "degree": form.get("degree", "B.Tech"),
                    "branch": form.get("branch", "Computer Science & Engineering"),
                    "current_year": safe_int(form.get("current_year"), 3),
                    "current_semester": safe_int(form.get("current_semester"), 5),
                    "cgpa": safe_float(form.get("cgpa"), 7.5),
                    "math_level": safe_int(form.get("math_level"), 6),
                    "stats_level": safe_int(form.get("stats_level"), 6),
                    "academic_performance": form.get("academic_performance", "Good")
                },
                "technical_skills": {
                    "python": safe_float(form.get("skill_python"), 5.0),
                    "java": safe_float(form.get("skill_java"), 5.0),
                    "c": safe_float(form.get("skill_c"), 4.0),
                    "cpp": safe_float(form.get("skill_cpp"), 4.0),
                    "javascript": safe_float(form.get("skill_javascript"), 5.0),
                    "sql": safe_float(form.get("skill_sql"), 5.0),
                    "html_css": safe_float(form.get("skill_html_css"), 5.0),
                    "machine_learning": safe_float(form.get("skill_machine_learning"), 4.0),
                    "deep_learning": safe_float(form.get("skill_deep_learning"), 3.0),
                    "data_analysis": safe_float(form.get("skill_data_analysis"), 5.0),
                    "cloud": safe_float(form.get("skill_cloud"), 4.0),
                    "cybersecurity": safe_float(form.get("skill_cybersecurity"), 4.0),
                    "networking": safe_float(form.get("skill_networking"), 4.0),
                    "database": safe_float(form.get("skill_database"), 5.0),
                    "git_github": safe_float(form.get("skill_git_github"), 5.0)
                },
                "soft_skills": {
                    "communication": safe_float(form.get("soft_communication"), 6.0),
                    "leadership": safe_float(form.get("soft_leadership"), 5.0),
                    "teamwork": safe_float(form.get("soft_teamwork"), 6.0),
                    "problem_solving": safe_float(form.get("soft_problem_solving"), 6.0),
                    "analytical_thinking": safe_float(form.get("soft_analytical_thinking"), 6.0),
                    "creativity": safe_float(form.get("soft_creativity"), 5.0),
                    "presentation": safe_float(form.get("soft_presentation"), 5.0),
                    "time_management": safe_float(form.get("soft_time_management"), 6.0)
                },
                "interests": form.getlist("interests") if hasattr(form, "getlist") else [],
                "experience": {
                    "projects_count": safe_int(form.get("projects_count"), 2),
                    "internship": form.get("internship", "no") == "yes",
                    "work_experience": form.get("work_experience", "no") == "yes",
                    "hackathons": safe_int(form.get("hackathons"), 0),
                    "certifications_count": safe_int(form.get("certifications_count"), 1),
                    "open_source": form.get("open_source", "no") == "yes"
                },
                "work_preferences": {
                    "style": form.get("pref_style", "Technical"),
                    "environment": form.get("pref_environment", "Hybrid"),
                    "organization": form.get("pref_org", "Enterprise"),
                    "stability": form.get("pref_stability", "Innovation"),
                    "team": form.get("pref_team", "Team")
                },
                "career_preferences": {
                    "desired_career": form.get("desired_career", "")
                }
            }

        result = process_student_assessment(g.user.id, raw_data)

        if request.is_json:
            return jsonify({
                "status": "success",
                "assessment_id": result["assessment_id"],
                "redirect_url": url_for("assessment.view_results", id=result["assessment_id"])
            })

        flash("Assessment processed with trained Machine Learning model!", "success")
        return redirect(url_for("assessment.view_results", id=result["assessment_id"]))

    except Exception as e:
        db.session.rollback()
        if request.is_json:
            return jsonify({"status": "error", "message": str(e)}), 500
        flash(f"Error processing assessment: {str(e)}", "danger")
        return redirect(url_for("assessment.wizard"))

@assessment_bp.route("/assessment/results/<int:id>")
@login_required
def view_results(id):
    assessment = Assessment.query.filter_by(id=id, user_id=g.user.id).first_or_404()
    prediction = Prediction.query.filter_by(assessment_id=id).first()
    explanation = PredictionExplanation.query.filter_by(prediction_id=prediction.id).first() if prediction else None
    skill_gap = SkillGap.query.filter_by(assessment_id=id).first()
    roadmap = Roadmap.query.filter_by(user_id=g.user.id, career_id=prediction.top_career_id).order_by(Roadmap.generated_at.desc()).first() if prediction else None

    # Scores breakdown
    raw = assessment.get_raw_responses()
    strengths = raw.get("strengths", ["Problem Solving", "Adaptability", "Python"])
    weaknesses = raw.get("weaknesses", ["Cloud Deployment", "Advanced Networking"])

    return render_template(
        "assessment/results.html",
        assessment=assessment,
        prediction=prediction,
        explanation=explanation,
        skill_gap=skill_gap,
        roadmap=roadmap,
        strengths=strengths,
        weaknesses=weaknesses
    )
