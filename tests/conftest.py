import pytest
import os
from pathlib import Path
from app import create_app
from database.db import db
from models.user import User
from models.profile import StudentProfile
from models.career import Career
from database.seed_manager import auto_seed_if_empty

class UserStub:
    def __init__(self, id, username, email, role):
        self.id = id
        self.username = username
        self.email = email
        self.role = role
        self.is_admin = (role == "admin")
        self.is_student = (role == "student")

@pytest.fixture(scope="session")
def app():
    """Create testing application context."""
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        auto_seed_if_empty()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture
def test_user(app):
    """Creates a regular student test user."""
    with app.app_context():
        user = User.query.filter_by(username="test_student").first()
        if not user:
            user = User(username="test_student", email="student@test.com", role="student")
            user.set_password("Student@123")
            db.session.add(user)
            db.session.flush()

            profile = StudentProfile(
                user_id=user.id,
                full_name="Test Student",
                college="National Institute of Technology",
                degree="B.Tech CSE",
                branch="Computer Science",
                cgpa=8.4,
                math_level=8,
                stats_level=8
            )
            db.session.add(profile)
            db.session.commit()
        return UserStub(user.id, user.username, user.email, user.role)

@pytest.fixture
def test_admin(app):
    """Creates an admin test user."""
    with app.app_context():
        admin = User.query.filter_by(username="test_admin").first()
        if not admin:
            admin = User(username="test_admin", email="admin@test.com", role="admin")
            admin.set_password("Admin@123")
            db.session.add(admin)
            db.session.commit()
        return UserStub(admin.id, admin.username, admin.email, admin.role)

@pytest.fixture
def auth_client(client, test_user):
    """Client logged in as student."""
    with client.session_transaction() as sess:
        sess["user_id"] = test_user.id
        sess["username"] = test_user.username
        sess["role"] = test_user.role
    return client

@pytest.fixture
def admin_client(client, test_admin):
    """Client logged in as admin."""
    with client.session_transaction() as sess:
        sess["user_id"] = test_admin.id
        sess["username"] = test_admin.username
        sess["role"] = test_admin.role
    return client
