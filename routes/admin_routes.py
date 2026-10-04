import json
from flask import Blueprint, render_template, request, redirect, url_for, flash, g
from database.db import db
from models.user import User
from models.career import Career, CareerSkill
from models.profile import Skill
from models.assessment import Assessment, Prediction
from models.resume import ModelVersion, ModelMetric, AdminLog
from ml.train import train_and_evaluate_models
from ml.predict import get_career_predictor
from routes.auth_routes import admin_required

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/admin")
@admin_required
def dashboard():
    total_users = User.query.count()
    total_students = User.query.filter_by(role="student").count()
    total_assessments = Assessment.query.count()
    total_careers = Career.query.count()
    total_skills = Skill.query.count()

    recent_users = User.query.order_by(User.created_at.desc()).limit(10).all()
    recent_assessments = Assessment.query.order_by(Assessment.created_at.desc()).limit(10).all()
    logs = AdminLog.query.order_by(AdminLog.created_at.desc()).limit(10).all()

    # Model metadata
    latest_model = ModelVersion.query.filter_by(is_active=1).first()

    return render_template(
        "admin/dashboard.html",
        total_users=total_users,
        total_students=total_students,
        total_assessments=total_assessments,
        total_careers=total_careers,
        total_skills=total_skills,
        recent_users=recent_users,
        recent_assessments=recent_assessments,
        logs=logs,
        latest_model=latest_model
    )

@admin_bp.route("/admin/careers", methods=["GET", "POST"])
@admin_required
def careers():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        code = request.form.get("code", "").strip().upper()
        category = request.form.get("category", "Software Engineering")
        desc = request.form.get("description", "").strip()
        qual = request.form.get("required_qualification", "B.Tech CSE")
        salary = request.form.get("average_salary_range", "₹6 - 15 LPA")
        difficulty = request.form.get("difficulty", "Intermediate")
        outlook = request.form.get("outlook", "High Demand")

        if title and code and desc:
            career = Career(
                title=title, code=code, category=category, description=desc,
                required_qualification=qual, average_salary_range=salary,
                difficulty=difficulty, outlook=outlook
            )
            db.session.add(career)
            
            # Log admin action
            log = AdminLog(admin_id=g.user.id, action="CREATE_CAREER", details=f"Added new career: {title} ({code})", ip_address=request.remote_addr)
            db.session.add(log)
            db.session.commit()
            flash(f"Career '{title}' created successfully.", "success")
        else:
            flash("Title, code, and description are required.", "danger")

        return redirect(url_for("admin.careers"))

    all_careers = Career.query.order_by(Career.title.asc()).all()
    skills = Skill.query.order_by(Skill.name.asc()).all()
    return render_template("admin/careers.html", careers=all_careers, skills=skills)

@admin_bp.route("/admin/train", methods=["POST"])
@admin_required
def trigger_training():
    try:
        train_result = train_and_evaluate_models()
        best_name = train_result["best_model_name"]
        m = train_result["metrics"]
        meta = train_result["metadata"]

        # Deactivate older models
        ModelVersion.query.update({ModelVersion.is_active: 0})

        # Save new ModelVersion
        version_tag = f"v{ModelVersion.query.count() + 1}.0.0"
        model_ver = ModelVersion(
            version_tag=version_tag,
            model_name=f"CareerAI-{best_name}",
            algorithm_name=best_name,
            accuracy=m["accuracy"],
            f1_score=m["f1_weighted"],
            precision_score=m["precision_weighted"],
            recall_score=m["recall_weighted"],
            is_active=1,
            trained_by=g.user.username,
            dataset_records=meta["total_records"]
        )
        db.session.add(model_ver)
        db.session.flush()

        # Model metrics
        metric_rec = ModelMetric(
            model_version_id=model_ver.id,
            metrics_json=json.dumps(train_result["comparison"]),
            confusion_matrix_json=json.dumps(meta["confusion_matrix"]),
            feature_importance_json=json.dumps(meta["feature_importances"])
        )
        db.session.add(metric_rec)

        # Log
        log = AdminLog(
            admin_id=g.user.id,
            action="TRAIN_MODEL",
            details=f"Retrained ML pipeline. Champion: {best_name} (Acc: {m['accuracy']*100:.1f}%, F1: {m['f1_weighted']*100:.1f}%)",
            ip_address=request.remote_addr
        )
        db.session.add(log)
        db.session.commit()

        # Reload predictor
        predictor = get_career_predictor()
        predictor._load_artifacts()

        flash(f"ML Pipeline retrained successfully! New champion model: {best_name} ({m['accuracy']*100:.1f}% accuracy).", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Training failed: {e}", "danger")

    return redirect(url_for("ml.analytics"))
