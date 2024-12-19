from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy


class User(db.Model, UserMixin):
    __tablename__ = "users"

    def __init__(self, email, name, password):
        self.email = email
        self.name = name
        self.password = password
    
    def get_id(self):
        return (self.user_id)

    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    name = db.Column(db.String(50))
    password = db.Column(db.String(150))


    def get_id(self):
        return (self.user_id)

    def __repr__(self):
        return f"id: {self.user_id}, email: {self.email}, name: {self.name}"
