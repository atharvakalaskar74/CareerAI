from datetime import datetime
from database.db import db

class Career(db.Model):
    __tablename__ = "careers"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    code = db.Column(db.String(50), nullable=False, unique=True, index=True)
    title = db.Column(db.String(150), nullable=False, unique=True, index=True)
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    required_qualification = db.Column(db.String(150))
    experience_level = db.Column(db.String(50), default="Entry Level")
    average_salary_range = db.Column(db.String(100))
    difficulty = db.Column(db.String(50), default="Intermediate")
    outlook = db.Column(db.String(100), default="High Demand")
    responsibilities = db.Column(db.Text)
    project_suggestions = db.Column(db.Text)
    is_active = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    skill_requirements = db.relationship("CareerSkill", backref="career", cascade="all, delete-orphan")
    roadmaps = db.relationship("Roadmap", backref="career", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "title": self.title,
            "category": self.category,
            "description": self.description,
            "required_qualification": self.required_qualification,
            "experience_level": self.experience_level,
            "average_salary_range": self.average_salary_range,
            "difficulty": self.difficulty,
            "outlook": self.outlook,
            "responsibilities": self.responsibilities.split("\n") if self.responsibilities else [],
            "project_suggestions": self.project_suggestions.split("\n") if self.project_suggestions else [],
            "is_active": bool(self.is_active)
        }

class CareerSkill(db.Model):
    __tablename__ = "career_skills"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    career_id = db.Column(db.Integer, db.ForeignKey("careers.id", ondelete="CASCADE"), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    required_level = db.Column(db.Integer, nullable=False, default=7)  # 0 to 10
    importance = db.Column(db.String(30), default="high")  # 'critical', 'high', 'medium', 'low'

    __table_args__ = (db.UniqueConstraint("career_id", "skill_id", name="_career_skill_uc"),)

    def to_dict(self):
        return {
            "id": self.id,
            "career_id": self.career_id,
            "career_title": self.career.title if self.career else None,
            "skill_id": self.skill_id,
            "skill_name": self.skill.name if self.skill else None,
            "category": self.skill.category if self.skill else None,
            "required_level": self.required_level,
            "importance": self.importance
        }
