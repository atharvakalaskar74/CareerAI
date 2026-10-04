import json
from datetime import datetime
from database.db import db

class ResumeAnalysis(db.Model):
    __tablename__ = "resume_analyses"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    extracted_text_preview = db.Column(db.Text)
    extracted_skills_json = db.Column(db.Text)
    extracted_education_json = db.Column(db.Text)
    extracted_experience_json = db.Column(db.Text)
    extracted_certifications_json = db.Column(db.Text)
    best_matched_career_id = db.Column(db.Integer, db.ForeignKey("careers.id", ondelete="SET NULL"), nullable=True)
    compatibility_score = db.Column(db.Float, default=0.0)
    gaps_json = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    best_career = db.relationship("Career")

    def to_dict(self):
        return {
            "id": self.id,
            "filename": self.filename,
            "extracted_skills": json.loads(self.extracted_skills_json) if self.extracted_skills_json else [],
            "extracted_education": json.loads(self.extracted_education_json) if self.extracted_education_json else [],
            "extracted_experience": json.loads(self.extracted_experience_json) if self.extracted_experience_json else [],
            "extracted_certifications": json.loads(self.extracted_certifications_json) if self.extracted_certifications_json else [],
            "best_matched_career": self.best_career.title if self.best_career else "General Tech Role",
            "compatibility_score": round(self.compatibility_score, 1),
            "gaps": json.loads(self.gaps_json) if self.gaps_json else [],
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M") if self.created_at else None
        }

class ModelVersion(db.Model):
    __tablename__ = "model_versions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    version_tag = db.Column(db.String(50), nullable=False, unique=True)
    model_name = db.Column(db.String(100), nullable=False)
    algorithm_name = db.Column(db.String(100), nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    f1_score = db.Column(db.Float, nullable=False)
    precision_score = db.Column(db.Float, nullable=False)
    recall_score = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Integer, default=0)
    trained_by = db.Column(db.String(100), default="System")
    dataset_records = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    metrics = db.relationship("ModelMetric", backref="version", uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "version_tag": self.version_tag,
            "model_name": self.model_name,
            "algorithm_name": self.algorithm_name,
            "accuracy": round(self.accuracy * 100, 2),
            "f1_score": round(self.f1_score * 100, 2),
            "precision_score": round(self.precision_score * 100, 2),
            "recall_score": round(self.recall_score * 100, 2),
            "is_active": bool(self.is_active),
            "trained_by": self.trained_by,
            "dataset_records": self.dataset_records,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M") if self.created_at else None
        }

class ModelMetric(db.Model):
    __tablename__ = "model_metrics"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    model_version_id = db.Column(db.Integer, db.ForeignKey("model_versions.id", ondelete="CASCADE"), nullable=False)
    metrics_json = db.Column(db.Text, nullable=False)
    confusion_matrix_json = db.Column(db.Text)
    feature_importance_json = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AdminLog(db.Model):
    __tablename__ = "admin_logs"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
