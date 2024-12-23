from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import User
from . import db
from datetime import datetime
import os, sys, re
import calendar

calendar.setfirstweekday(firstweekday=6)
views = Blueprint("views", __name__)

week = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']

# 計算行事曆的函數
def calc_calender(date):
    year = date.year
    yearInfo = dict()
    for month in range(1, 13):
        days = calendar.monthcalendar(year, month)
        if len(days) != 6:
            days.append([0 for _ in range(7)])
        month_addr = calendar.month_abbr[month]
        yearInfo[month_addr] = days
    return yearInfo

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)

@views.route("/calendar", methods=["GET", "POST"])
@login_required
def Calendar():
    if request.method == "POST":
        year = int(request.form.get('year'))
        date = datetime(year, 1, 1)
        if(year == datetime.today().year):
            date = datetime.today()
    else:
        date = datetime.today()

    this_month = calendar.month_abbr[date.month]
    return render_template('Calendar.html', this_month=this_month, date=date, content=calc_calender(date), user=current_user)
