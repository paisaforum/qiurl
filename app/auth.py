from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
from app import db, login_manager

bp = Blueprint("auth", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("routes.dashboard"))
        else:
            flash("Invalid credentials", "danger")
    return render_template("login.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))

@bp.route("/register", methods=["POST"])
@login_required
def register():
    if not current_user.is_admin:
        return "Unauthorized", 403

    email = request.form["email"]
    password = request.form["password"]

    if User.query.filter_by(email=email).first():
        flash("User already exists", "warning")
        return redirect(url_for("routes.dashboard"))

    user = User(email=email, is_admin=False)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    flash("User registered!", "success")
    return redirect(url_for("routes.dashboard"))
