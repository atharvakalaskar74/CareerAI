from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import logging

db = SQLAlchemy()
logger = logging.getLogger(__name__)

def init_db(app):
    """Initialize the database with the Flask app."""
    db.init_app(app)
    with app.app_context():
        # Create all defined models
        db.create_all()
        # Seed initial data if tables are empty
        from database.seed_manager import auto_seed_if_empty
        auto_seed_if_empty()
