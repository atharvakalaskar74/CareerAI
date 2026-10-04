from services.skill_gap_service import calculate_skill_gaps_for_career
from models.career import Career

def test_skill_gap_calculation(app):
    with app.app_context():
        # Get AI/ML Engineer
        aiml = Career.query.filter_by(code="AIML_ENG").first()
        assert aiml is not None

        # Student with high Python but low Deep Learning
        student_skills = {
            "python": 9.0,
            "machine_learning": 8.0,
            "deep_learning": 2.0,  # Required is 7 -> missing
            "sql": 5.0,            # Required is 7 -> weak
            "problem_solving": 8.0
        }

        gap_res = calculate_skill_gaps_for_career(aiml.id, student_skills)
        assert gap_res is not None
        assert "matched_skills" in gap_res
        assert "weak_skills" in gap_res
        assert "missing_skills" in gap_res
        assert gap_res["gap_score"] > 0.0

        # Check that Deep Learning is classified as missing
        missing_names = [m["skill_name"] for m in gap_res["missing_skills"]]
        assert "Deep Learning" in missing_names

        # Check that Python is classified as matched
        matched_names = [m["skill_name"] for m in gap_res["matched_skills"]]
        assert "Python" in matched_names
