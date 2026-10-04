from services.roadmap_service import generate_personalized_roadmap
from models.career import Career

def test_roadmap_generation(app):
    with app.app_context():
        career = Career.query.filter_by(code="DATA_SCI").first()
        assert career is not None

        student_skills = {
            "python": 8.0,
            "sql": 7.0,
            "data_analysis": 5.0, # Weak
            "machine_learning": 3.0 # Missing
        }

        roadmap = generate_personalized_roadmap(career.id, student_skills)
        assert roadmap is not None
        assert len(roadmap["phases"]) == 6
        assert roadmap["total_months"] >= 3
        
        # Verify 6 phase names
        phase_names = [p["phase_name"] for p in roadmap["phases"]]
        assert "Foundation & Prerequisites" in phase_names[0]
        assert "Core Technical Mastery" in phase_names[1]
        assert "Advanced Specialization" in phase_names[2]
        assert "Portfolio & Capstone Projects" in phase_names[3]
        assert "Deployment, DevOps & Cloud" in phase_names[4]
        assert "Interview Preparation & Career Readiness" in phase_names[5]

        # Verify resources exist in phases
        for p in roadmap["phases"]:
            assert "resources" in p
            assert len(p["resources"]) >= 1
