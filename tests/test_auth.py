from models.user import User

def test_password_hashing(app):
    with app.app_context():
        user = User(username="hash_test", email="hash@test.com")
        user.set_password("Secret123")
        assert user.password_hash != "Secret123"
        assert user.check_password("Secret123") is True
        assert user.check_password("WrongSecret") is False

def test_user_registration(client, app):
    response = client.post("/register", data={
        "username": "new_student",
        "email": "new_student@college.edu",
        "password": "Password123",
        "confirm_password": "Password123",
        "full_name": "New Student",
        "college": "Test College",
        "degree": "B.Tech CSE"
    }, follow_redirects=True)
    assert response.status_code == 200
    with app.app_context():
        user = User.query.filter_by(username="new_student").first()
        assert user is not None
        assert user.email == "new_student@college.edu"
        assert user.role == "student"

def test_registration_duplicate_username(client):
    # Attempt to register existing user
    response = client.post("/register", data={
        "username": "new_student",
        "email": "another@college.edu",
        "password": "Password123",
        "confirm_password": "Password123"
    }, follow_redirects=True)
    assert b"Username is already taken" in response.data

def test_login_and_logout(client, test_user):
    # Valid login
    res = client.post("/login", data={
        "identifier": "test_student",
        "password": "Student@123"
    }, follow_redirects=True)
    assert res.status_code == 200
    assert b"Welcome back, test_student" in res.data

    # Logout
    res_logout = client.get("/logout", follow_redirects=True)
    assert res_logout.status_code == 200
    assert b"signed out successfully" in res_logout.data

def test_invalid_login(client):
    res = client.post("/login", data={
        "identifier": "nonexistent_user",
        "password": "WrongPassword"
    }, follow_redirects=True)
    assert b"Invalid username/email or password" in res.data

def test_protected_routes_unauthenticated(client):
    res = client.get("/dashboard", follow_redirects=False)
    assert res.status_code == 302
    assert "/login" in res.headers["Location"]
