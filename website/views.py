from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import User
from . import db
from datetime import datetime
import os, sys, re

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)



@views.route("/spin_the_wheel")
def spin_the_wheel():
    return render_template("spin_the_wheel.html", user=current_user)