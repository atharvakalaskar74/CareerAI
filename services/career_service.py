from models.career import Career, CareerSkill
from models.profile import Skill
from services.skill_gap_service import calculate_skill_gaps_for_career

def get_all_careers(category=None, search=None):
    """Retrieves all active careers with optional filtering."""
    query = Career.query.filter_by(is_active=1)
    if category and category != "All":
        query = query.filter_by(category=category)
    if search:
        search_term = f"%{search}%"
        query = query.filter(Career.title.ilike(search_term) | Career.description.ilike(search_term))
    return query.order_by(Career.title.asc()).all()

def compare_careers(career_ids, student_skills_dict=None):
    """
    Compares 2 to 3 careers side-by-side, generating detailed comparative
    matrices and Chart.js radar data.
    """
    student_skills_dict = student_skills_dict or {}
    careers = Career.query.filter(Career.id.in_(career_ids)).all()
    if not careers:
        return None

    comparison_items = []
    all_skill_names = set()

    for career in careers:
        gap_info = calculate_skill_gaps_for_career(career.id, student_skills_dict)
        reqs = CareerSkill.query.filter_by(career_id=career.id).all()
        for r in reqs:
            if r.skill:
                all_skill_names.add(r.skill.name)

        comparison_items.append({
            "career": career.to_dict(),
            "match_percentage": gap_info["match_percentage"] if gap_info else 0,
            "gap_score": gap_info["gap_score"] if gap_info else 0,
            "matched_count": len(gap_info["matched_skills"]) if gap_info else 0,
            "weak_count": len(gap_info["weak_skills"]) if gap_info else 0,
            "missing_count": len(gap_info["missing_skills"]) if gap_info else 0,
            "missing_skills": [m["skill_name"] for m in gap_info["missing_skills"][:4]] if gap_info else [],
            "requirements": {r.skill.name: r.required_level for r in reqs if r.skill}
        })

    # Pick top 8 most distinguishing skills for radar chart
    radar_labels = sorted(list(all_skill_names))[:8]

    radar_datasets = []
    # 1. Student level dataset
    student_data = []
    for skill_name in radar_labels:
        key = skill_name.lower().replace("/", "_").replace(" ", "_").replace("-", "_")
        val = float(student_skills_dict.get(key, student_skills_dict.get(skill_name, 5.0)))
        student_data.append(val)

    radar_datasets.append({
        "label": "Your Current Level",
        "data": student_data,
        "backgroundColor": "rgba(99, 102, 241, 0.2)",
        "borderColor": "rgba(99, 102, 241, 1)",
        "pointBackgroundColor": "rgba(99, 102, 241, 1)"
    })

    # 2. Career requirement datasets
    colors = [
        {"bg": "rgba(16, 185, 129, 0.2)", "border": "rgba(16, 185, 129, 1)"},
        {"bg": "rgba(245, 158, 11, 0.2)", "border": "rgba(245, 158, 11, 1)"},
        {"bg": "rgba(239, 68, 68, 0.2)", "border": "rgba(239, 68, 68, 1)"}
    ]

    for idx, item in enumerate(comparison_items):
        req_data = []
        for skill_name in radar_labels:
            req_data.append(item["requirements"].get(skill_name, 0))
        
        c = colors[idx % len(colors)]
        radar_datasets.append({
            "label": f"Required: {item['career']['title']}",
            "data": req_data,
            "backgroundColor": c["bg"],
            "borderColor": c["border"],
            "pointBackgroundColor": c["border"]
        })

    return {
        "careers": comparison_items,
        "radar_chart": {
            "labels": radar_labels,
            "datasets": radar_datasets
        }
    }
