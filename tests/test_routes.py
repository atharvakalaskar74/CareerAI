def test_landing_page(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"CareerAI" in res.data
    assert b"Featured Tech Careers" in res.data

def test_career_explorer_and_detail(client):
    res = client.get("/careers")
    assert res.status_code == 200
    assert b"Tech Career Library" in res.data

    res_detail = client.get("/careers/1")
    assert res_detail.status_code == 200
    assert b"Role Overview" in res_detail.data

def test_career_comparison(client):
    res = client.get("/careers/compare?c1=1&c2=2")
    assert res.status_code == 200
    assert b"Side-by-Side Career Comparison" in res.data

def test_ml_analytics_route(client):
    res = client.get("/ml-analytics")
    assert res.status_code == 200
    assert b"Machine Learning Analytics Dashboard" in res.data

def test_assessment_flow(auth_client):
    # GET wizard
    res_get = auth_client.get("/assessment")
    assert res_get.status_code == 200
    assert b"Career Assessment Assessment" in res_get.data

    # POST submission
    post_data = {
        "highest_qualification": "Undergraduate",
        "degree": "B.Tech CSE",
        "branch": "AI & ML",
        "current_year": 3,
        "current_semester": 5,
        "cgpa": 8.5,
        "math_level": 9,
        "stats_level": 9,
        "academic_performance": "Excellent",
        "skill_python": 9.0,
        "skill_java": 4.0,
        "skill_c": 4.0,
        "skill_cpp": 4.0,
        "skill_javascript": 4.0,
        "skill_sql": 8.0,
        "skill_html_css": 4.0,
        "skill_machine_learning": 9.0,
        "skill_deep_learning": 8.5,
        "skill_data_analysis": 8.5,
        "skill_cloud": 6.0,
        "skill_cybersecurity": 4.0,
        "skill_networking": 4.0,
        "skill_database": 7.0,
        "skill_git_github": 8.0,
        "soft_communication": 7.0,
        "soft_leadership": 6.0,
        "soft_teamwork": 8.0,
        "soft_problem_solving": 9.0,
        "soft_analytical_thinking": 9.0,
        "soft_creativity": 7.0,
        "soft_presentation": 7.0,
        "soft_time_management": 7.0,
        "projects_count": 3,
        "internship": "yes",
        "work_experience": "no",
        "hackathons": 2,
        "certifications_count": 2,
        "open_source": "yes",
        "pref_style": "Technical",
        "pref_environment": "Hybrid",
        "pref_org": "Startup",
        "pref_stability": "Innovation",
        "pref_team": "Team"
    }

    res_post = auth_client.post("/assessment/submit", data=post_data, follow_redirects=True)
    assert res_post.status_code == 200
    assert b"Career Compatibility & Intelligence Report" in res_post.data

def test_admin_authorization_denied_for_student(auth_client):
    res_denied = auth_client.get("/admin", follow_redirects=True)
    assert b"Administrator privileges required" in res_denied.data

def test_admin_authorization_granted_for_admin(admin_client):
    res_admin = admin_client.get("/admin")
    assert res_admin.status_code == 200
    assert b"Admin Control Center" in res_admin.data
