from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from database.db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True, index=True)
    email = db.Column(db.String(150), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="student", index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profile = db.relationship("StudentProfile", backref="user", uselist=False, cascade="all, delete-orphan")
    skills = db.relationship("StudentSkill", backref="user", cascade="all, delete-orphan")
    interests = db.relationship("StudentInterest", backref="user", cascade="all, delete-orphan")
    education = db.relationship("Education", backref="user", cascade="all, delete-orphan")
    projects = db.relationship("Project", backref="user", cascade="all, delete-orphan")
    certifications = db.relationship("Certification", backref="user", cascade="all, delete-orphan")
    assessments = db.relationship("Assessment", backref="user", cascade="all, delete-orphan")
    predictions = db.relationship("Prediction", backref="user", cascade="all, delete-orphan")
    roadmaps = db.relationship("Roadmap", backref="user", cascade="all, delete-orphan")
    progress_records = db.relationship("ProgressRecord", backref="user", cascade="all, delete-orphan")
    resume_analyses = db.relationship("ResumeAnalysis", backref="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == "admin"

    @property
    def is_student(self):
        return self.role == "student"

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
