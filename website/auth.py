from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, login_required, logout_user
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint("auth", __name__)

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        if User.query.filter_by(email=email).first():
            flash("Email is already in use.", category="error")
        elif User.query.filter_by(name=name).first():
            flash("User name is already in use.", category="error")
        elif len(password1) < 6:
            flash("Password should be at least 6 characters.", category="error")
        elif password1 != password2:
            flash("Passwords don\'t match.", category="error")
        else:
            user = User(email, name, generate_password_hash(password1))
            db.session.add(user)
            db.session.commit()

            login_user(user, remember=True)
            flash("User created.", category="success")
            return redirect(url_for("views.home"))


    return render_template("signup.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))


@auth.route("/login", methods=["GET", "POST"])
def login():
    email = ""
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Logged in.", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password incorrect.", category="error")

        else:
            flash("User does not exist.", category="error")

    return render_template("login.html", user=current_user, last_email=email)
