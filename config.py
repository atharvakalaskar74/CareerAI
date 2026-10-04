import os
from datetime import timedelta
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
# Load environment variables from .env if present
load_dotenv(BASE_DIR / ".env")

def resolve_database_uri():
    """
    Resolves the SQLAlchemy database URI dynamically:
    1. Checks DATABASE_URL (normalizes mysql:// to mysql+pymysql://).
    2. Checks granular DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT.
    3. Falls back to local SQLite in instance/careerai.db.
    """
    raw_url = os.getenv("DATABASE_URL")
    if raw_url:
        if raw_url.startswith("mysql://"):
            return raw_url.replace("mysql://", "mysql+pymysql://", 1)
        elif raw_url.startswith("postgres://"):
            return raw_url.replace("postgres://", "postgresql://", 1)
        elif raw_url.startswith("sqlite:///"):
            path_part = raw_url[len("sqlite:///"):]
            if path_part and not os.path.isabs(path_part) and not path_part.startswith(":memory:"):
                resolved = (BASE_DIR / path_part).resolve().as_posix()
                return f"sqlite:///{resolved}"
        return raw_url

    # Check granular MySQL environment variables
    db_host = os.getenv("DB_HOST")
    if db_host:
        db_user = os.getenv("DB_USER", "root")
        db_pass = os.getenv("DB_PASSWORD", "")
        db_port = os.getenv("DB_PORT", "3306")
        db_name = os.getenv("DB_NAME", "careerai_db")
        auth = f"{db_user}:{db_pass}" if db_pass else db_user
        return f"mysql+pymysql://{auth}@{db_host}:{db_port}/{db_name}?charset=utf8mb4"

    # Default fallback: SQLite for zero-config local development
    instance_dir = BASE_DIR / "instance"
    instance_dir.mkdir(exist_ok=True)
    instance_db = (instance_dir / "careerai.db").resolve().as_posix()
    return f"sqlite:///{instance_db}"

class Config:
    """Base configuration settings for CareerAI."""
    SECRET_KEY = os.getenv("SECRET_KEY", "careerai_super_secret_production_key_btech_cse_2026")
    
    SQLALCHEMY_DATABASE_URI = resolve_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Connection pool options for resilient cloud database connections
    if "mysql" in SQLALCHEMY_DATABASE_URI or "postgres" in SQLALCHEMY_DATABASE_URI:
        SQLALCHEMY_ENGINE_OPTIONS = {
            "pool_pre_ping": True,
            "pool_recycle": 280,
            "pool_timeout": 30
        }
    else:
        SQLALCHEMY_ENGINE_OPTIONS = {}

    # File uploads
    UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", str(BASE_DIR / "uploads" / "resumes"))
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))  # 16 MB
    ALLOWED_EXTENSIONS = {"pdf"}
    
    # ML settings
    MODEL_DIR = os.getenv("MODEL_DIR", str(BASE_DIR / "ml" / "saved_models"))
    DATASET_DIR = str(BASE_DIR / "ml" / "dataset")
    DEFAULT_RANDOM_STATE = int(os.getenv("DEFAULT_RANDOM_STATE", 42))

    # Session settings
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

class DevelopmentConfig(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    DEBUG = False
    # Set to True on HTTPS cloud platforms (Render, Railway, etc.)
    SESSION_COOKIE_SECURE = os.getenv("SESSION_COOKIE_SECURE", "true").lower() == "true"
    PREFERRED_URL_SCHEME = "https"

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SQLALCHEMY_ENGINE_OPTIONS = {}
    WTF_CSRF_ENABLED = False
    SESSION_COOKIE_SECURE = False

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig
}
