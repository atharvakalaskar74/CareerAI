from .auth_routes import auth_bp
from .student_routes import student_bp
from .assessment_routes import assessment_bp
from .career_routes import career_bp
from .simulation_routes import simulation_bp
from .resume_routes import resume_bp
from .admin_routes import admin_bp
from .ml_routes import ml_bp

__all__ = [
    "auth_bp",
    "student_bp",
    "assessment_bp",
    "career_bp",
    "simulation_bp",
    "resume_bp",
    "admin_bp",
    "ml_bp"
]
