import io
from services.resume_parser_service import parse_resume_text, match_resume_to_careers

def test_resume_parser_keyword_matching(app):
    with app.app_context():
        sample_resume_text = """
        John Doe — B.Tech Computer Science and Engineering
        Skills: Python, Machine Learning, Deep Learning, SQL, Pandas, Git, PyTorch
        Projects: Built an End-to-End Object Detection System using PyTorch and OpenCV.
        Experience: Completed 6 months software internship at Tech Corp.
        """
        parsed = parse_resume_text(sample_resume_text)
        assert "Python" in parsed["extracted_skills"]
        assert "Machine Learning" in parsed["extracted_skills"]
        assert "Deep Learning" in parsed["extracted_skills"]

        matches = match_resume_to_careers(parsed["extracted_skills"])
        assert matches is not None
        assert matches["best_career"]["career_title"] in ["AI/ML Engineer", "Data Scientist", "AI Researcher"]

def test_resume_invalid_file_extension(auth_client):
    data = {
        "resume": (io.BytesIO(b"dummy text content"), "resume.txt")
    }
    res = auth_client.post("/resume/upload", data=data, content_type="multipart/form-data", follow_redirects=True)
    assert b"Only official PDF documents" in res.data
