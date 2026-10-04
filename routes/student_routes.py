from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from database.db import db
from models.user import User
from models.profile import StudentProfile, StudentSkill, Skill
from models.assessment import Assessment, Prediction, ProgressRecord, Roadmap
from models.career import Career
from routes.auth_routes import login_required

student_bp = Blueprint("student", __name__)

@student_bp.route("/dashboard")
@login_required
def dashboard():
    latest_assessment = Assessment.query.filter_by(user_id=g.user.id).order_by(Assessment.created_at.desc()).first()
    latest_prediction = Prediction.query.filter_by(user_id=g.user.id).order_by(Prediction.created_at.desc()).first()
    active_roadmap = Roadmap.query.filter_by(user_id=g.user.id).order_by(Roadmap.generated_at.desc()).first()
    progress_count = ProgressRecord.query.filter_by(user_id=g.user.id).count()
    
    # User skills count
    skills_count = StudentSkill.query.filter_by(user_id=g.user.id).count()

    return render_template(
        "dashboard/index.html",
        user=g.user,
        profile=g.user.profile,
        assessment=latest_assessment,
        prediction=latest_prediction,
        roadmap=active_roadmap,
        progress_count=progress_count,
        skills_count=skills_count
    )

@student_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    user_profile = g.user.profile
    if not user_profile:
        user_profile = StudentProfile(user_id=g.user.id)
        db.session.add(user_profile)
        db.session.commit()

    if request.method == "POST":
        user_profile.full_name = request.form.get("full_name", "").strip()
        user_profile.phone = request.form.get("phone", "").strip()
        user_profile.college = request.form.get("college", "").strip()
        user_profile.degree = request.form.get("degree", "").strip()
        user_profile.branch = request.form.get("branch", "").strip()
        user_profile.current_year = int(request.form.get("current_year", 3))
        user_profile.current_semester = int(request.form.get("current_semester", 5))
        user_profile.cgpa = float(request.form.get("cgpa", user_profile.cgpa or 7.0))
        user_profile.work_preference_style = request.form.get("work_preference_style", "Technical")
        user_profile.work_environment = request.form.get("work_environment", "Hybrid")
        user_profile.org_preference = request.form.get("org_preference", "Enterprise")
        user_profile.bio = request.form.get("bio", "").strip()

        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("student.profile"))

    # Fetch skills
    student_skills = StudentSkill.query.filter_by(user_id=g.user.id).all()
    return render_template("dashboard/profile.html", user=g.user, profile=user_profile, skills=student_skills)

@student_bp.route("/progress")
@login_required
def progress():
    records = ProgressRecord.query.filter_by(user_id=g.user.id).order_by(ProgressRecord.recorded_at.asc()).all()
    
    chart_dates = [r.recorded_at.strftime("%b %d") for r in records]
    chart_readiness = [round(r.career_readiness_score, 1) for r in records]
    chart_compat = [round(r.top_compatibility, 1) for r in records]

    return render_template(
        "progress/timeline.html",
        records=list(reversed(records)),
        chart_dates=chart_dates,
        chart_readiness=chart_readiness,
        chart_compat=chart_compat
    )
