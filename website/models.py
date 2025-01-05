from flask import Flask, render_template, request, jsonify
from flask_login import UserMixin
from . import db
from sqlalchemy.sql import func
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


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

    def get_email(self):
        return (self.email)

    def __repr__(self):
        return f"id: {self.user_id}, email: {self.email}, name: {self.name}"

class Event(db.Model):
    def __init__(self, email, title, start, notification):
        self.email = email
        self.title = title
        self.start = start
        self.notification = notification
        self.sent = False

    event_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    # start = db.Column(db.String(100), nullable=False)
    # end = db.Column(db.String(100), nullable=False)
    start = db.Column(db.String(100))
    notification = db.Column(db.String(100))
    sent = db.Column(db.Boolean)
