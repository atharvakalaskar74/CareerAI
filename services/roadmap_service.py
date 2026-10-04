from models.career import Career
from services.skill_gap_service import calculate_skill_gaps_for_career
from database.db import db

def generate_personalized_roadmap(career_id, student_skill_dict, experience_info=None):
    """
    Generates a personalized 6-phase career acceleration roadmap
    tailored dynamically to the student's evaluated skill gaps,
    target career role, and practical experience level.
    """
    career = db.session.get(Career, career_id)
    if not career:
        return None

    gap_data = calculate_skill_gaps_for_career(career_id, student_skill_dict)
    missing = [m["skill_name"] for m in gap_data["missing_skills"]]
    weak = [w["skill_name"] for w in gap_data["weak_skills"]]
    matched = [m["skill_name"] for m in gap_data["matched_skills"]]

    experience_info = experience_info or {}
    project_cnt = int(experience_info.get("projects_count", 0))

    # Phase duration multipliers based on gap severity
    pace_factor = 1.2 if len(missing) >= 4 else (0.8 if len(missing) <= 1 else 1.0)

    # 1. Phase 1: Foundation
    phase1_skills = [s for s in weak + missing if s in ["Python", "Java", "C", "C++", "Mathematics", "Statistics", "HTML/CSS"]]
    if not phase1_skills:
        phase1_skills = ["Core Programming Foundations", "Problem Solving Refinement"]
    phase1 = {
        "phase_number": 1,
        "phase_name": "Foundation & Prerequisites",
        "title": f"Reinforcing Core {career.title} Foundations",
        "description": f"Solidify mathematical reasoning, algorithmic logic, and fundamental syntax required for {career.title}.",
        "skills_targeted": phase1_skills,
        "resources": [
            {"title": "CS50 Introduction to Computer Science", "type": "Course", "url": "https://cs50.harvard.edu/"},
            {"title": "Kaggle Python & Pandas Micro-Courses", "type": "Interactive", "url": "https://www.kaggle.com/learn"}
        ],
        "estimated_weeks": max(2, int(4 * pace_factor))
    }

    # 2. Phase 2: Core Skills
    phase2_skills = [s for s in missing if s not in phase1_skills][:3]
    if not phase2_skills:
        phase2_skills = [s for s in weak if s not in phase1_skills][:3]
    if not phase2_skills:
        phase2_skills = ["Domain Architecture", "Core Tooling"]
    phase2 = {
        "phase_number": 2,
        "phase_name": "Core Technical Mastery",
        "title": f"Bridging Critical Competency Gaps in {', '.join(phase2_skills[:2])}",
        "description": f"Deep dive into standard libraries, frameworks, and practical problem sets directly addressing your highest priority gaps.",
        "skills_targeted": phase2_skills,
        "resources": [
            {"title": "Official Framework Documentation & Best Practices", "type": "Documentation", "url": "https://docs.python.org/"},
            {"title": "Hands-on Guided Technical Labs", "type": "Labs", "url": "https://github.com/"}
        ],
        "estimated_weeks": max(3, int(6 * pace_factor))
    }

    # 3. Phase 3: Advanced Skills
    phase3_skills = [s for s in missing + weak if s not in phase1_skills and s not in phase2_skills]
    if not phase3_skills:
        phase3_skills = ["Advanced Optimization", "System Architecture", "Security Best Practices"]
    phase3 = {
        "phase_number": 3,
        "phase_name": "Advanced Specialization",
        "title": f"Production-Grade Specialization for {career.title}",
        "description": "Master advanced topics such as distributed systems, model optimization, latency minimization, and scalable design.",
        "skills_targeted": phase3_skills[:3],
        "resources": [
            {"title": "Designing Data-Intensive Applications", "type": "Book", "url": "https://dataintensive.net/"},
            {"title": "Advanced Engineering Masterclasses", "type": "Tutorials", "url": "https://ocw.mit.edu/"}
        ],
        "estimated_weeks": max(3, int(5 * pace_factor))
    }

    # 4. Phase 4: Applied Projects
    project_suggestions = career.project_suggestions.split("\n") if career.project_suggestions else [
        f"End-to-End {career.title} Production System with Testing and CI",
        "Full-Stack Domain Dashboard with Interactive Analytics"
    ]
    selected_projects = [p.strip() for p in project_suggestions if p.strip()][:2]
    phase4 = {
        "phase_number": 4,
        "phase_name": "Portfolio & Capstone Projects",
        "title": "Building Industry-Caliber Capstones",
        "description": f"Build non-trivial, deployable projects demonstrating practical mastery of {career.title} deliverables to recruiters.",
        "skills_targeted": ["Applied System Design", "Project Architecture", "Git Version Control"],
        "resources": [
            {"title": selected_projects[0] if selected_projects else "Capstone Project 1", "type": "Project Spec", "url": "https://github.com"},
            {"title": selected_projects[1] if len(selected_projects) > 1 else "Capstone Project 2", "type": "Project Spec", "url": "https://github.com"}
        ],
        "estimated_weeks": max(4, int(6 * pace_factor))
    }

    # 5. Phase 5: Deployment & Tooling
    phase5 = {
        "phase_number": 5,
        "phase_name": "Deployment, DevOps & Cloud",
        "title": "Production Deployment & Continuous Integration",
        "description": "Containerize applications with Docker, automate testing via GitHub Actions, and deploy services to free-tier cloud environments.",
        "skills_targeted": ["Docker", "Git/GitHub", "Cloud Deployment", "CI/CD Pipelines"],
        "resources": [
            {"title": "Docker Getting Started Guide", "type": "Docs", "url": "https://docs.docker.com/get-started/"},
            {"title": "Free Hosting Deployment Guides (Render / Vercel)", "type": "Guide", "url": "https://render.com/docs"}
        ],
        "estimated_weeks": 3
    }

    # 6. Phase 6: Career Preparation
    phase6 = {
        "phase_number": 6,
        "phase_name": "Interview Preparation & Career Readiness",
        "title": f"Technical Interviews & Portfolio Polish for {career.title}",
        "description": "Conduct mock technical interviews, refine system design explanations, optimize your resume keywords, and showcase your GitHub repositories.",
        "skills_targeted": ["Technical Communication", "System Design", "Behavioral Interviews", "Resume Optimization"],
        "resources": [
            {"title": "NeetCode / LeetCode Roadmap", "type": "Practice", "url": "https://neetcode.io/"},
            {"title": "Tech Interview Handbook", "type": "Guide", "url": "https://www.techinterviewhandbook.org/"}
        ],
        "estimated_weeks": 4
    }

    phases = [phase1, phase2, phase3, phase4, phase5, phase6]
    total_weeks = sum(p["estimated_weeks"] for p in phases)
    total_months = max(3, round(total_weeks / 4.0))

    return {
        "career_id": career.id,
        "career_title": career.title,
        "total_weeks": total_weeks,
        "total_months": total_months,
        "phases": phases,
        "summary": f"{total_months}-month structured progression tailored to resolve {len(missing)} missing and {len(weak)} weak competencies for {career.title}."
    }
