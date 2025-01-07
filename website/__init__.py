from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import datetime
import subprocess

db = SQLAlchemy()


def create_app():
    app = Flask(__name__, static_url_path="/static")
    app.config["SECRET_KEY"] = "iwonttellyou"
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
    db.init_app(app)

    from .models import User

    with app.app_context():
        db.create_all()

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(idx):
        return User.query.get(int(idx))

    subprocess.Popen(["python", "send_email.py"])
    return app
