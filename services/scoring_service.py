def calculate_profile_scores(raw_responses):
    """
    Computes application-level student profile indicator scores (0 - 100).
    Explicitly documented as derived heuristic indices based on multi-criteria inputs.
    """
    academic = raw_responses.get("academic", {})
    tech_skills = raw_responses.get("technical_skills", {})
    soft_skills = raw_responses.get("soft_skills", {})
    experience = raw_responses.get("experience", {})

    # 1. Academic Foundation Score (0 - 100)
    cgpa = float(academic.get("cgpa", 7.0))
    math_val = float(academic.get("math_level", 5.0))
    stats_val = float(academic.get("stats_level", 5.0))
    # CGPA is on 10-point scale
    academic_score = (
        (cgpa / 10.0) * 50.0 +
        (math_val / 10.0) * 25.0 +
        (stats_val / 10.0) * 25.0
    )
    academic_score = round(min(100.0, max(0.0, academic_score)), 1)

    # 2. Technical Skill Score (0 - 100)
    tech_vals = [float(v) for v in tech_skills.values() if v is not None]
    if tech_vals:
        tech_score = round((sum(tech_vals) / (len(tech_vals) * 10.0)) * 100.0, 1)
    else:
        tech_score = 50.0

    # 3. Soft Skill Score (0 - 100)
    soft_vals = [float(v) for v in soft_skills.values() if v is not None]
    if soft_vals:
        soft_score = round((sum(soft_vals) / (len(soft_vals) * 10.0)) * 100.0, 1)
    else:
        soft_score = 50.0

    # 4. Problem Solving Score (0 - 100)
    ps_val = float(soft_skills.get("problem_solving", 6.0))
    at_val = float(soft_skills.get("analytical_thinking", 6.0))
    da_val = float(tech_skills.get("data_analysis", 5.0))
    problem_solving_score = round(
        ((ps_val * 0.4 + at_val * 0.4 + da_val * 0.2) / 10.0) * 100.0, 1
    )

    # 5. Practical Experience Score (0 - 100)
    projects_cnt = int(experience.get("projects_count", 0))
    internship = 1 if experience.get("internship") in [True, "yes", "Yes", 1, "1"] else 0
    work_exp = 1 if experience.get("work_experience") in [True, "yes", "Yes", 1, "1"] else 0
    hackathons = int(experience.get("hackathons", 0))
    certs = int(experience.get("certifications_count", 0))
    open_source = 1 if experience.get("open_source") in [True, "yes", "Yes", 1, "1"] else 0

    exp_points = (
        min(projects_cnt * 10.0, 30.0) +
        (internship * 25.0) +
        (work_exp * 15.0) +
        min(hackathons * 5.0, 10.0) +
        min(certs * 5.0, 10.0) +
        (open_source * 10.0)
    )
    practical_score = round(min(100.0, max(10.0, exp_points)), 1)

    # 6. Overall Career Readiness Score (0 - 100)
    # Weighted composition
    career_readiness = round(
        (tech_score * 0.35) +
        (problem_solving_score * 0.20) +
        (academic_score * 0.15) +
        (practical_score * 0.15) +
        (soft_score * 0.15),
        1
    )

    # Identify Strengths & Weaknesses
    all_rated_skills = {**tech_skills, **soft_skills}
    sorted_skills = sorted(all_rated_skills.items(), key=lambda x: float(x[1] or 0), reverse=True)
    strengths = [s[0].replace("_", " ").title() for s in sorted_skills if float(s[1] or 0) >= 7.0][:5]
    weaknesses = [s[0].replace("_", " ").title() for s in reversed(sorted_skills) if float(s[1] or 0) <= 5.0][:5]

    return {
        "academic_foundation_score": academic_score,
        "technical_score": tech_score,
        "soft_skill_score": soft_score,
        "problem_solving_score": problem_solving_score,
        "practical_experience_score": practical_score,
        "career_readiness_score": career_readiness,
        "strengths": strengths if strengths else ["Foundational Programming", "Adaptability"],
        "weaknesses": weaknesses if weaknesses else ["Production Deployment", "Advanced Architecture"]
    }
