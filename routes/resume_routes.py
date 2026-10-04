import os
import json
from pathlib import Path
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, g
from werkzeug.utils import secure_filename
from database.db import db
from models.resume import ResumeAnalysis
from models.career import Career
from services.resume_parser_service import extract_text_from_pdf, parse_resume_text, match_resume_to_careers
from routes.auth_routes import login_required

resume_bp = Blueprint("resume", __name__)

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in {"pdf"}

@resume_bp.route("/resume")
@login_required
def view_resume_page():
    past_analyses = ResumeAnalysis.query.filter_by(user_id=g.user.id).order_by(ResumeAnalysis.created_at.desc()).all()
    latest = past_analyses[0] if past_analyses else None
    return render_template("resume/upload.html", latest=latest, past_analyses=past_analyses)

@resume_bp.route("/resume/upload", methods=["POST"])
@login_required
def upload_resume():
    if "resume" not in request.files:
        flash("No file part provided in request.", "danger")
        return redirect(url_for("resume.view_resume_page"))

    file = request.files["resume"]
    if file.filename == "":
        flash("No file selected for upload.", "warning")
        return redirect(url_for("resume.view_resume_page"))

    if not allowed_file(file.filename):
        flash("Invalid file format. Only official PDF documents (.pdf) are supported.", "danger")
        return redirect(url_for("resume.view_resume_page"))

    # Secure filename and directory setup
    safe_name = secure_filename(file.filename)
    upload_dir = Path(current_app.config["UPLOAD_FOLDER"])
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    unique_filename = f"{g.user.id}_{int(os.times().system*1000)}_{safe_name}"
    save_path = upload_dir / unique_filename
    file.save(str(save_path))

    # Extract text locally
    extracted_text = extract_text_from_pdf(str(save_path))
    if not extracted_text:
        flash("Could not parse text from this PDF. Please ensure it is not password protected or a scanned image.", "danger")
        return redirect(url_for("resume.view_resume_page"))

    # Parse sections
    parsed = parse_resume_text(extracted_text)
    
    # Match against database careers
    matches = match_resume_to_careers(parsed["extracted_skills"])
    best_match = matches["best_career"] if matches else None

    # Save to database
    analysis = ResumeAnalysis(
        user_id=g.user.id,
        filename=safe_name,
        extracted_text_preview=extracted_text[:600] + "...",
        extracted_skills_json=json.dumps(parsed["extracted_skills"]),
        extracted_education_json=json.dumps(parsed["extracted_education"]),
        extracted_experience_json=json.dumps(parsed["extracted_experience"]),
        extracted_certifications_json=json.dumps(parsed["extracted_projects"] + parsed["extracted_certifications"]),
        best_matched_career_id=best_match["career_id"] if best_match else None,
        compatibility_score=best_match["compatibility_score"] if best_match else 0.0,
        gaps_json=json.dumps(best_match["missing_skills"] if best_match else [])
    )
    db.session.add(analysis)
    db.session.commit()

    flash("Resume parsed and analyzed successfully against tech career benchmarks!", "success")
    return redirect(url_for("resume.view_resume_page"))
