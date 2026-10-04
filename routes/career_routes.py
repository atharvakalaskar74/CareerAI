from flask import Blueprint, render_template, request, redirect, url_for, flash, g, jsonify
from database.db import db
from models.career import Career, CareerSkill
from models.profile import StudentSkill
from models.assessment import Assessment, Prediction, Roadmap, SkillGap
from services.career_service import get_all_careers, compare_careers
from services.skill_gap_service import calculate_skill_gaps_for_career
from services.roadmap_service import generate_personalized_roadmap
from routes.auth_routes import login_required

career_bp = Blueprint("career", __name__)

def get_student_skills_map(user_id):
    """Helper to get student's current rated skills dictionary."""
    skills = StudentSkill.query.filter_by(user_id=user_id).all()
    res = {}
    for s in skills:
        if s.skill:
            key = s.skill.name.lower().replace("/", "_").replace(" ", "_").replace("-", "_")
            res[key] = s.proficiency_level
            res[s.skill.name] = s.proficiency_level
    # Fallback to latest assessment responses if student_skills empty
    if not res:
        latest = Assessment.query.filter_by(user_id=user_id).order_by(Assessment.created_at.desc()).first()
        if latest:
            raw = latest.get_raw_responses()
            tech = raw.get("technical_skills", {})
            soft = raw.get("soft_skills", {})
            res = {**tech, **soft}
    return res

@career_bp.route("/careers")
def explorer():
    category = request.args.get("category", "All")
    search = request.args.get("search", "").strip()
    careers = get_all_careers(category=category, search=search)
    categories = ["All", "AI & Data Science", "Software Engineering", "Web Engineering", "Security & Infrastructure", "Cloud & Systems", "Design & Product", "Data Infrastructure", "Data Analytics"]
    return render_template("careers/explorer.html", careers=careers, selected_category=category, search_query=search, categories=categories)

@career_bp.route("/careers/<int:id>")
def detail(id):
    career = db.get_or_404(Career, id)
    skills = CareerSkill.query.filter_by(career_id=id).all()
    
    # Check student match if logged in
    student_gap = None
    if g.user:
        s_skills = get_student_skills_map(g.user.id)
        if s_skills:
            student_gap = calculate_skill_gaps_for_career(id, s_skills)

    return render_template("careers/detail.html", career=career, skills=skills, student_gap=student_gap)

@career_bp.route("/careers/<int:id>/gap")
@login_required
def skill_gap(id):
    career = db.get_or_404(Career, id)
    s_skills = get_student_skills_map(g.user.id)
    
    if not s_skills:
        flash("Please complete the assessment first to calculate your skill gaps.", "info")
        return redirect(url_for("assessment.wizard"))

    gap_data = calculate_skill_gaps_for_career(id, s_skills)
    return render_template("careers/skill_gap.html", career=career, gap_data=gap_data)

@career_bp.route("/careers/compare", methods=["GET", "POST"])
def compare():
    all_careers = Career.query.filter_by(is_active=1).order_by(Career.title.asc()).all()
    selected_ids = []

    if request.method == "POST":
        selected_ids = [int(i) for i in request.form.getlist("career_ids") if i.isdigit()]
    else:
        # Query params
        c1 = request.args.get("c1")
        c2 = request.args.get("c2")
        c3 = request.args.get("c3")
        for c in [c1, c2, c3]:
            if c and c.isdigit():
                selected_ids.append(int(c))

    # Default to comparing top 2 if none selected
    if len(selected_ids) < 2 and len(all_careers) >= 2:
        selected_ids = [all_careers[0].id, all_careers[1].id]

    s_skills = get_student_skills_map(g.user.id) if g.user else {}
    comparison = compare_careers(selected_ids[:3], s_skills)

    return render_template(
        "careers/compare.html",
        all_careers=all_careers,
        selected_ids=selected_ids,
        comparison=comparison
    )

@career_bp.route("/careers/target", methods=["GET", "POST"])
@login_required
def target_career():
    all_careers = Career.query.filter_by(is_active=1).order_by(Career.title.asc()).all()
    selected_career_id = request.args.get("career_id") or request.form.get("career_id")

    if not selected_career_id and all_careers:
        selected_career_id = all_careers[0].id
    else:
        selected_career_id = int(selected_career_id)

    target = db.session.get(Career, selected_career_id)
    s_skills = get_student_skills_map(g.user.id)
    
    if not s_skills:
        flash("Complete an assessment to analyze your target career readiness.", "info")
        return redirect(url_for("assessment.wizard"))

    gap_data = calculate_skill_gaps_for_career(target.id, s_skills)
    roadmap = generate_personalized_roadmap(target.id, s_skills)

    return render_template(
        "careers/target.html",
        all_careers=all_careers,
        target=target,
        gap_data=gap_data,
        roadmap=roadmap
    )

@career_bp.route("/roadmap/<int:career_id>")
@login_required
def view_roadmap(career_id):
    career = db.get_or_404(Career, career_id)
    s_skills = get_student_skills_map(g.user.id)
    roadmap = generate_personalized_roadmap(career_id, s_skills)
    return render_template("roadmap/view.html", career=career, roadmap=roadmap)
