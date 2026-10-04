import os
import logging
from flask import Flask, render_template, jsonify, g, redirect, url_for
from sqlalchemy import text
from config import config_by_name
from database import db, init_db
from models.career import Career
from models.user import User

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("careerai")

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name["development"]))

    # Initialize Database
    init_db(app)

    # Preload and warm the trained ML Model in memory
    with app.app_context():
        try:
            from ml.predict import get_career_predictor
            predictor = get_career_predictor()
            if not predictor.is_ready():
                predictor._load_artifacts()
            logger.info("CareerAI ML Model loaded successfully into memory.")
        except Exception as e:
            logger.warning(f"ML Model deferred warm-up notice: {e}")

    # Register Blueprints
    from routes import (
        auth_bp, student_bp, assessment_bp,
        career_bp, simulation_bp, resume_bp,
        admin_bp, ml_bp
    )
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(assessment_bp)
    app.register_blueprint(career_bp)
    app.register_blueprint(simulation_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(ml_bp)

    @app.route("/")
    def index():
        featured_careers = Career.query.filter_by(is_active=1).limit(6).all()
        return render_template("index.html", featured_careers=featured_careers)

    @app.route("/health")
    def health_check():
        """Production Health Probe verifying Web, DB, and ML core status."""
        db_status = "connected"
        try:
            db.session.execute(text("SELECT 1"))
        except Exception as e:
            db_status = f"unhealthy: {type(e).__name__}"

        from ml.predict import get_career_predictor
        predictor = get_career_predictor()
        ml_ready = predictor.is_ready()

        is_healthy = (db_status == "connected") and ml_ready
        status_code = 200 if is_healthy else 503

        return jsonify({
            "status": "healthy" if is_healthy else "degraded",
            "service": "CareerAI — Intelligent Career Recommendation Engine",
            "database": db_status,
            "ml_engine": "ready" if ml_ready else "initializing",
            "environment": os.getenv("FLASK_ENV", "production")
        }), status_code

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("base.html", error_title="Page Not Found (404)", error_message="The requested resource could not be found."), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        logger.error(f"Internal server error: {error}")
        return render_template("base.html", error_title="Internal System Error (500)", error_message="An unexpected system error occurred. The technical team has been notified."), 500

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug_mode = os.getenv("FLASK_ENV", "development") == "development"
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
