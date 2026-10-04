from models.career import Career, CareerSkill
from models.profile import Skill
from database.db import db

def calculate_skill_gaps_for_career(career_id, student_skill_dict):
    """
    Compares the student's evaluated skill levels against the database-defined
    skill requirements for the designated career role.
    Categorizes skills into:
    - matched: student_level >= required_level
    - weak: required_level - 2 <= student_level < required_level
    - missing: student_level < required_level - 2
    """
    career = db.session.get(Career, career_id)
    if not career:
        return None

    requirements = CareerSkill.query.filter_by(career_id=career_id).all()
    
    matched_skills = []
    weak_skills = []
    missing_skills = []
    
    total_required_pts = 0
    total_student_pts = 0

    for req in requirements:
        skill_name = req.skill.name if req.skill else f"Skill #{req.skill_id}"
        # Normalize key for lookup
        key = skill_name.lower().replace("/", "_").replace(" ", "_").replace("-", "_")
        
        # Student skill level (default 4.0 if not rated)
        student_level = float(student_skill_dict.get(key, student_skill_dict.get(skill_name, 4.0)))
        required_level = float(req.required_level)
        importance = req.importance or "high"

        total_required_pts += required_level
        total_student_pts += min(student_level, required_level)

        item = {
            "skill_id": req.skill_id,
            "skill_name": skill_name,
            "category": req.skill.category if req.skill else "technical",
            "student_level": student_level,
            "required_level": required_level,
            "gap": round(required_level - student_level, 1),
            "importance": importance
        }

        if student_level >= required_level:
            item["status"] = "Strong / Matched"
            item["priority"] = "Low Priority (Maintain)"
            matched_skills.append(item)
        elif student_level >= (required_level - 2.0):
            item["status"] = "Moderate / Needs Polish"
            item["priority"] = "Medium Priority" if importance in ["critical", "high"] else "Low Priority"
            weak_skills.append(item)
        else:
            item["status"] = "Critical Gap / Missing"
            item["priority"] = "High Priority" if importance in ["critical", "high"] else "Medium Priority"
            missing_skills.append(item)

    # Sort gaps by importance & size of gap
    importance_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    weak_skills.sort(key=lambda x: (importance_order.get(x["importance"], 2), -x["gap"]))
    missing_skills.sort(key=lambda x: (importance_order.get(x["importance"], 2), -x["gap"]))

    # Overall gap percentage (0% = perfect match, 100% = max gap)
    if total_required_pts > 0:
        gap_score = round(max(0.0, (1.0 - (total_student_pts / total_required_pts)) * 100.0), 1)
        match_percentage = round(100.0 - gap_score, 1)
    else:
        gap_score = 0.0
        match_percentage = 100.0

    return {
        "career_id": career.id,
        "career_code": career.code,
        "career_title": career.title,
        "matched_skills": matched_skills,
        "weak_skills": weak_skills,
        "missing_skills": missing_skills,
        "gap_score": gap_score,
        "match_percentage": match_percentage,
        "total_skills_evaluated": len(requirements)
    }
