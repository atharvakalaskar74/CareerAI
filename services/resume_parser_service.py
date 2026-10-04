import os
import re
import logging
from pathlib import Path
from pypdf import PdfReader
from werkzeug.utils import secure_filename
from models.career import Career, CareerSkill
from models.profile import Skill

logger = logging.getLogger(__name__)

# Standard skill keywords dictionary for local pattern matching
TECH_SKILL_PATTERNS = {
    "Python": [r"\bpython\b", r"\bflask\b", r"\bdjango\b", r"\bfastapi\b", r"\bpandas\b", r"\bnumpy\b"],
    "Java": [r"\bjava\b", r"\bspring boot\b", r"\bjvm\b", r"\bhibernate\b"],
    "C": [r"\bc\b", r"\bembedded c\b"],
    "C++": [r"\bc\+\+\b", r"\bcpp\b", r"\bstl\b"],
    "JavaScript": [r"\bjavascript\b", r"\bjs\b", r"\btypescript\b", r"\breact\b", r"\bnode\b", r"\bvue\b", r"\bangular\b"],
    "SQL": [r"\bsql\b", r"\bmysql\b", r"\bpostgresql\b", r"\boracle\b", r"\bsqlite\b", r"\bqueries\b"],
    "HTML/CSS": [r"\bhtml5?\b", r"\bcss3?\b", r"\btailwind\b", r"\bbootstrap\b", r"\bsass\b"],
    "Machine Learning": [r"\bmachine learning\b", r"\bml\b", r"\bscikit-learn\b", r"\bsklearn\b", r"\bclassification\b", r"\bregression\b"],
    "Deep Learning": [r"\bdeep learning\b", r"\bpytorch\b", r"\btensorflow\b", r"\bkeras\b", r"\bneural networks\b", r"\bcnn\b", r"\brnn\b", r"\btransformer\b"],
    "Data Analysis": [r"\bdata analysis\b", r"\beda\b", r"\bpower bi\b", r"\btableau\b", r"\bexcel\b", r"\bvisualization\b"],
    "Cloud": [r"\baws\b", r"\bazure\b", r"\bgcp\b", r"\bgoogle cloud\b", r"\bcloud computing\b", r"\bec2\b", r"\bs3\b"],
    "Cybersecurity": [r"\bcybersecurity\b", r"\bsecurity\b", r"\bpenetration testing\b", r"\bwireshark\b", r"\bcryptography\b", r"\bowasp\b"],
    "Networking": [r"\bnetworking\b", r"\btcp/ip\b", r"\bosi\b", r"\bdns\b", r"\brouting\b", r"\bhttp\b", r"\bprotocols\b"],
    "Database": [r"\bdatabase\b", r"\bmongodb\b", r"\bredis\b", r"\brdbms\b", r"\bnosql\b", r"\bdatabase design\b"],
    "Git/GitHub": [r"\bgit\b", r"\bgithub\b", r"\bgitlab\b", r"\bversion control\b", r"\bci/cd\b"]
}

EDUCATION_PATTERNS = [
    r"\b(?:b\.?tech|bachelor of technology|b\.?e|bachelor of engineering|m\.?tech|bca|mca|b\.?sc|m\.?sc)\b",
    r"\b(?:computer science|information technology|data science|artificial intelligence|cse|ai & ml)\b"
]

def extract_text_from_pdf(filepath):
    """Safely extracts raw text from a PDF file using local pypdf."""
    try:
        reader = PdfReader(filepath)
        text_pages = []
        for page in reader.pages:
            t = page.extract_text()
            if t:
                text_pages.append(t)
        full_text = "\n".join(text_pages)
        return full_text.strip()
    except Exception as e:
        logger.error(f"PDF extraction error: {e}")
        return ""

def parse_resume_text(raw_text):
    """
    Parses resume text locally using regex keyword matching.
    Extracts skills, education, certifications, and experience mentions.
    Fields without sufficient certainty are clearly marked as uncertain.
    """
    lowered = raw_text.lower()
    
    # 1. Skill Extraction
    extracted_skills = []
    for skill_name, patterns in TECH_SKILL_PATTERNS.items():
        for pat in patterns:
            if re.search(pat, lowered):
                extracted_skills.append(skill_name)
                break

    # 2. Education Extraction
    extracted_edu = []
    for pat in EDUCATION_PATTERNS:
        matches = re.findall(pat, lowered)
        if matches:
            for m in set(matches):
                extracted_edu.append(m.upper())

    # 3. Project keywords search
    project_matches = re.findall(r"(?:project|built|developed|created|implemented)\s*:\s*([^\n\.\;]+)", raw_text, re.IGNORECASE)
    extracted_projects = [p.strip() for p in project_matches[:4] if len(p.strip()) > 5]

    # 4. Certifications search
    cert_matches = re.findall(r"(?:certified|certification|certificate|credential)\s*:\s*([^\n\.\;]+)", raw_text, re.IGNORECASE)
    extracted_certs = [c.strip() for c in cert_matches[:4] if len(c.strip()) > 4]

    # 5. Experience / Internship detection
    has_internship = bool(re.search(r"\b(?:intern|internship|trainee|apprentice)\b", lowered))
    has_experience = bool(re.search(r"\b(?:experience|work history|employment|developer at|engineer at)\b", lowered))
    
    experience_status = []
    if has_internship:
        experience_status.append("Internship experience identified")
    if has_experience:
        experience_status.append("Work/industry experience section identified")
    if not experience_status:
        experience_status.append("Entry-level / No verified industry experience detected (Uncertain)")

    return {
        "extracted_skills": extracted_skills,
        "extracted_education": extracted_edu if extracted_edu else ["Degree details detected from profile (Uncertain from text)"],
        "extracted_projects": extracted_projects if extracted_projects else ["Project listings mentioned in document"],
        "extracted_certifications": extracted_certs if extracted_certs else ["No formal certificates explicitly parsed"],
        "extracted_experience": experience_status
    }

def match_resume_to_careers(extracted_skills):
    """
    Matches extracted skills against all database careers to determine
    the best-fit career role, compatibility score, and missing skills.
    """
    all_careers = Career.query.all()
    if not all_careers:
        return None

    results = []
    for career in all_careers:
        reqs = CareerSkill.query.filter_by(career_id=career.id).all()
        required_skill_names = [r.skill.name for r in reqs if r.skill]
        
        if not required_skill_names:
            continue

        matched = [s for s in required_skill_names if s in extracted_skills]
        missing = [s for s in required_skill_names if s not in extracted_skills]
        
        # Compatibility score
        score = round((len(matched) / len(required_skill_names)) * 100.0, 1)

        results.append({
            "career_id": career.id,
            "career_title": career.title,
            "career_code": career.code,
            "compatibility_score": score,
            "matched_skills": matched,
            "missing_skills": missing,
            "total_required": len(required_skill_names)
        })

    if not results:
        return None

    # Sort descending
    results.sort(key=lambda x: x["compatibility_score"], reverse=True)
    best_match = results[0] if results else None

    return {
        "best_career": best_match,
        "all_career_matches": results[:5]
    }
