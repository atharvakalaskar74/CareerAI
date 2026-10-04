import os
from flask import Flask, render_template, g, redirect, url_for
from config import config_by_name
from database import db, init_db
from models.career import Career
from models.user import User

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name["development"]))

    # Initialize Database
    init_db(app)

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

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template("base.html", error_title="Page Not Found (404)", error_message="The requested resource could not be found."), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("base.html", error_title="Internal System Error (500)", error_message="An unexpected system error occurred. The technical team has been notified."), 500

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
