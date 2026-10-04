from datetime import datetime
from database.db import db

class StudentProfile(db.Model):
    __tablename__ = "student_profiles"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    full_name = db.Column(db.String(150))
    phone = db.Column(db.String(30))
    college = db.Column(db.String(200))
    degree = db.Column(db.String(100))
    branch = db.Column(db.String(100))
    current_year = db.Column(db.Integer, default=1)
    current_semester = db.Column(db.Integer, default=1)
    cgpa = db.Column(db.Float, default=0.0)
    math_level = db.Column(db.Integer, default=5)
    stats_level = db.Column(db.Integer, default=5)
    academic_performance = db.Column(db.String(50), default="Good")
    work_preference_style = db.Column(db.String(50), default="Technical")
    work_environment = db.Column(db.String(50), default="Hybrid")
    org_preference = db.Column(db.String(50), default="Enterprise")
    risk_preference = db.Column(db.String(50), default="Innovation")
    team_preference = db.Column(db.String(50), default="Team")
    bio = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "full_name": self.full_name,
            "phone": self.phone,
            "college": self.college,
            "degree": self.degree,
            "branch": self.branch,
            "current_year": self.current_year,
            "current_semester": self.current_semester,
            "cgpa": self.cgpa,
            "math_level": self.math_level,
            "stats_level": self.stats_level,
            "academic_performance": self.academic_performance,
            "work_preference_style": self.work_preference_style,
            "work_environment": self.work_environment,
            "org_preference": self.org_preference,
            "risk_preference": self.risk_preference,
            "team_preference": self.team_preference,
            "bio": self.bio
        }

class Skill(db.Model):
    __tablename__ = "skills"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    category = db.Column(db.String(50), nullable=False, index=True)  # 'technical', 'soft', 'tool'
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    career_requirements = db.relationship("CareerSkill", backref="skill", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description
        }

class StudentSkill(db.Model):
    __tablename__ = "student_skills"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    skill_id = db.Column(db.Integer, db.ForeignKey("skills.id", ondelete="CASCADE"), nullable=False)
    proficiency_level = db.Column(db.Integer, nullable=False, default=5)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    skill = db.relationship("Skill")
    __table_args__ = (db.UniqueConstraint("user_id", "skill_id", name="_user_skill_uc"),)

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "skill_id": self.skill_id,
            "skill_name": self.skill.name if self.skill else None,
            "category": self.skill.category if self.skill else None,
            "proficiency_level": self.proficiency_level
        }

class Interest(db.Model):
    __tablename__ = "interests"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    category = db.Column(db.String(50), default="Technology")
    description = db.Column(db.Text)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description
        }

class StudentInterest(db.Model):
    __tablename__ = "student_interests"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    interest_id = db.Column(db.Integer, db.ForeignKey("interests.id", ondelete="CASCADE"), nullable=False)

    interest = db.relationship("Interest")
    __table_args__ = (db.UniqueConstraint("user_id", "interest_id", name="_user_interest_uc"),)

class Education(db.Model):
    __tablename__ = "education"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    qualification = db.Column(db.String(100), nullable=False)
    degree = db.Column(db.String(150))
    institution = db.Column(db.String(200))
    score_percentage = db.Column(db.Float)
    graduation_year = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Project(db.Model):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))
    tech_stack = db.Column(db.Text)
    description = db.Column(db.Text)
    project_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Certification(db.Model):
    __tablename__ = "certifications"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    issuer = db.Column(db.String(150))
    issue_date = db.Column(db.String(50))
    credential_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
