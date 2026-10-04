import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

class Config:
    """Base configuration settings for CareerAI."""
    SECRET_KEY = os.getenv("SECRET_KEY", "careerai_super_secret_production_key_btech_cse_2026")
    
    # Database config: default to SQLite in instance/ directory if MySQL is not set up
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL or DATABASE_URL.startswith("sqlite"):
        instance_dir = BASE_DIR / "instance"
        instance_dir.mkdir(exist_ok=True)
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{instance_dir / 'careerai.db'}"
    else:
        SQLALCHEMY_DATABASE_URI = DATABASE_URL

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # File uploads
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(BASE_DIR / "uploads" / "resumes"))
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))  # 16 MB
    ALLOWED_EXTENSIONS = {"pdf"}
    
    # ML settings
    MODEL_DIR = os.getenv("MODEL_DIR", str(BASE_DIR / "ml" / "saved_models"))
    DATASET_DIR = str(BASE_DIR / "ml" / "dataset")
    DEFAULT_RANDOM_STATE = int(os.getenv("DEFAULT_RANDOM_STATE", 42))

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
