def test_what_if_simulation_api(auth_client):
    baseline = {
        "python": 5.0, "java": 5.0, "c": 4.0, "cpp": 4.0, "javascript": 5.0,
        "sql": 5.0, "html_css": 5.0, "machine_learning": 3.0, "deep_learning": 2.0,
        "data_analysis": 5.0, "cloud": 4.0, "cybersecurity": 4.0, "networking": 4.0,
        "database": 5.0, "git_github": 5.0, "problem_solving": 6.0,
        "analytical_thinking": 6.0, "communication": 6.0, "math_level": 6.0,
        "stats_level": 6.0, "cgpa": 7.5
    }

    # Simulate boosting Machine Learning & Deep Learning to 9.5
    simulated = baseline.copy()
    simulated["python"] = 9.0
    simulated["machine_learning"] = 9.5
    simulated["deep_learning"] = 9.0
    simulated["math_level"] = 9.0
    simulated["stats_level"] = 9.0

    res = auth_client.post("/api/simulate", json={
        "baseline": baseline,
        "simulated": simulated
    })

    assert res.status_code == 200
    data = res.get_json()
    assert data["status"] == "success"
    assert "before" in data
    assert "after" in data
    assert "shifts" in data

    # Check that after prediction shifts toward AI/ML or Data Science
    assert data["after"]["top_career"] in ["AI/ML Engineer", "Data Scientist", "AI Researcher"]
