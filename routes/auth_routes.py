from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, g
from database.db import db
from models.user import User
from models.profile import StudentProfile

auth_bp = Blueprint("auth", __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in to access this page.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user_id" not in session:
            flash("Please sign in as administrator.", "warning")
            return redirect(url_for("auth.login", next=request.path))
        user = db.session.get(User, session["user_id"])
        if not user or not user.is_admin:
            flash("Administrator privileges required.", "danger")
            return redirect(url_for("student.dashboard"))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.before_app_request
def load_logged_in_user():
    user_id = session.get("user_id")
    if user_id is None:
        g.user = None
    else:
        g.user = db.session.get(User, user_id)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if g.user:
        return redirect(url_for("student.dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")
        full_name = request.form.get("full_name", "").strip()
        college = request.form.get("college", "").strip()
        degree = request.form.get("degree", "B.Tech CSE")

        # Validation
        if not username or not email or not password:
            flash("All mandatory fields are required.", "danger")
            return render_template("auth/register.html")

        if len(password) < 6:
            flash("Password must be at least 6 characters long.", "danger")
            return render_template("auth/register.html")

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return render_template("auth/register.html")

        if User.query.filter_by(username=username).first():
            flash("Username is already taken. Please choose another.", "danger")
            return render_template("auth/register.html")

        if User.query.filter_by(email=email).first():
            flash("Email is already registered. Please sign in.", "danger")
            return render_template("auth/register.html")

        # Create user & profile
        user = User(username=username, email=email, role="student")
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        profile = StudentProfile(
            user_id=user.id,
            full_name=full_name or username,
            college=college,
            degree=degree,
            current_year=3,
            current_semester=5
        )
        db.session.add(profile)
        db.session.commit()

        flash("Registration successful! You can now sign in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("auth/register.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if g.user:
        return redirect(url_for("student.dashboard"))

    if request.method == "POST":
        identifier = request.form.get("identifier", "").strip()
        password = request.form.get("password", "")
        remember = bool(request.form.get("remember"))

        user = User.query.filter((User.username == identifier) | (User.email == identifier.lower())).first()

        if user and user.check_password(password):
            session.clear()
            session["user_id"] = user.id
            session["role"] = user.role
            session["username"] = user.username
            if remember:
                session.permanent = True

            flash(f"Welcome back, {user.username}!", "success")
            next_url = request.args.get("next")
            if user.is_admin:
                return redirect(next_url or url_for("admin.dashboard"))
            return redirect(next_url or url_for("student.dashboard"))
        else:
            flash("Invalid username/email or password.", "danger")

    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been signed out successfully.", "info")
    return redirect(url_for("auth.login"))
