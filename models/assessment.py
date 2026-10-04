import json
from datetime import datetime
from database.db import db

class Assessment(db.Model):
    __tablename__ = "assessments"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    academic_foundation_score = db.Column(db.Float, default=0.0)
    technical_score = db.Column(db.Float, default=0.0)
    soft_skill_score = db.Column(db.Float, default=0.0)
    problem_solving_score = db.Column(db.Float, default=0.0)
    practical_experience_score = db.Column(db.Float, default=0.0)
    career_readiness_score = db.Column(db.Float, default=0.0)
    raw_responses_json = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    prediction = db.relationship("Prediction", backref="assessment", uselist=False, cascade="all, delete-orphan")

    def get_raw_responses(self):
        return json.loads(self.raw_responses_json) if self.raw_responses_json else {}

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "academic_foundation_score": round(self.academic_foundation_score, 1),
            "technical_score": round(self.technical_score, 1),
            "soft_skill_score": round(self.soft_skill_score, 1),
            "problem_solving_score": round(self.problem_solving_score, 1),
            "practical_experience_score": round(self.practical_experience_score, 1),
            "career_readiness_score": round(self.career_readiness_score, 1),
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M") if self.created_at else None
        }

class Prediction(db.Model):
    __tablename__ = "predictions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessments.id", ondelete="CASCADE"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    top_career_id = db.Column(db.Integer, db.ForeignKey("careers.id", ondelete="CASCADE"), nullable=False)
    top_career_code = db.Column(db.String(50), nullable=False)
    compatibility_score = db.Column(db.Float, nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    top_predictions_json = db.Column(db.Text, nullable=False)  # List of {career_id, title, score}
    model_version = db.Column(db.String(50), default="v1.0.0")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    top_career = db.relationship("Career")
    explanation = db.relationship("PredictionExplanation", backref="prediction", uselist=False, cascade="all, delete-orphan")

    def get_top_predictions(self):
        return json.loads(self.top_predictions_json) if self.top_predictions_json else []

    def to_dict(self):
        return {
            "id": self.id,
            "assessment_id": self.assessment_id,
            "top_career": self.top_career.title if self.top_career else self.top_career_code,
            "top_career_code": self.top_career_code,
            "compatibility_score": round(self.compatibility_score, 1),
            "confidence_score": round(self.confidence_score, 1),
            "top_predictions": self.get_top_predictions(),
            "model_version": self.model_version,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M") if self.created_at else None
        }

class PredictionExplanation(db.Model):
    __tablename__ = "prediction_explanations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    prediction_id = db.Column(db.Integer, db.ForeignKey("predictions.id", ondelete="CASCADE"), nullable=False)
    top_positive_features_json = db.Column(db.Text)
    top_negative_features_json = db.Column(db.Text)
    feature_importances_json = db.Column(db.Text)
    human_readable_summary = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "positive_features": json.loads(self.top_positive_features_json) if self.top_positive_features_json else [],
            "negative_features": json.loads(self.top_negative_features_json) if self.top_negative_features_json else [],
            "feature_importances": json.loads(self.feature_importances_json) if self.feature_importances_json else {},
            "human_readable_summary": self.human_readable_summary
        }

class SkillGap(db.Model):
    __tablename__ = "skill_gaps"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    career_id = db.Column(db.Integer, db.ForeignKey("careers.id", ondelete="CASCADE"), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessments.id", ondelete="SET NULL"), nullable=True)
    matched_skills_json = db.Column(db.Text)
    weak_skills_json = db.Column(db.Text)
    missing_skills_json = db.Column(db.Text)
    gap_score = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    career = db.relationship("Career")

    def to_dict(self):
        return {
            "id": self.id,
            "career_id": self.career_id,
            "career_title": self.career.title if self.career else "",
            "matched_skills": json.loads(self.matched_skills_json) if self.matched_skills_json else [],
            "weak_skills": json.loads(self.weak_skills_json) if self.weak_skills_json else [],
            "missing_skills": json.loads(self.missing_skills_json) if self.missing_skills_json else [],
            "gap_score": round(self.gap_score, 1)
        }

class Roadmap(db.Model):
    __tablename__ = "roadmaps"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    career_id = db.Column(db.Integer, db.ForeignKey("careers.id", ondelete="CASCADE"), nullable=False)
    target_completion_months = db.Column(db.Integer, default=6)
    generated_at = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship("RoadmapItem", backref="roadmap", cascade="all, delete-orphan", order_by="RoadmapItem.order_index")

class RoadmapItem(db.Model):
    __tablename__ = "roadmap_items"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    roadmap_id = db.Column(db.Integer, db.ForeignKey("roadmaps.id", ondelete="CASCADE"), nullable=False)
    phase_number = db.Column(db.Integer, nullable=False)
    phase_name = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    skills_targeted_json = db.Column(db.Text)
    resources_json = db.Column(db.Text)
    estimated_weeks = db.Column(db.Integer, default=4)
    order_index = db.Column(db.Integer, default=1)

    def to_dict(self):
        return {
            "phase_number": self.phase_number,
            "phase_name": self.phase_name,
            "title": self.title,
            "description": self.description,
            "skills_targeted": json.loads(self.skills_targeted_json) if self.skills_targeted_json else [],
            "resources": json.loads(self.resources_json) if self.resources_json else [],
            "estimated_weeks": self.estimated_weeks
        }

class CareerComparison(db.Model):
    __tablename__ = "career_comparisons"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    compared_career_ids_json = db.Column(db.Text, nullable=False)
    comparison_data_json = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class ProgressRecord(db.Model):
    __tablename__ = "progress_records"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    assessment_id = db.Column(db.Integer, db.ForeignKey("assessments.id", ondelete="SET NULL"), nullable=True)
    career_readiness_score = db.Column(db.Float, nullable=False)
    top_career_title = db.Column(db.String(150), nullable=False)
    top_compatibility = db.Column(db.Float, nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "career_readiness_score": round(self.career_readiness_score, 1),
            "top_career_title": self.top_career_title,
            "top_compatibility": round(self.top_compatibility, 1),
            "date": self.recorded_at.strftime("%b %d, %Y")
        }
