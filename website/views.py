from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import User, Event
from . import db
from datetime import datetime, timedelta
import os, sys, re
import calendar
from random import randrange

calendar.setfirstweekday(firstweekday=6)
views = Blueprint("views", __name__)

week = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']

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

events = {}
@views.route("/calendar", methods=["GET", "POST"])
@login_required
def Calendar():
    date = datetime.today()

    if request.method == "POST":
        form_id = request.form.get('form_id')

        if form_id == 'update_year':
            year = int(request.form.get('year'))
            date = datetime(year, 1, 1)
            if year == datetime.today().year:
                date = datetime.today()

        elif form_id == 'add_event':
            event_date = request.form.get('eventDate')
            notification_time = request.form.get('notification_time')
            event = request.form.get('eventText')
            submit_type = request.form.get('submit_type')
            print(event_date, event)
            
            new_event = Event(current_user.get_email(), event, datetime.strptime(event_date, '%Y-%m-%dT%H:%M'), datetime.strptime(notification_time, '%Y-%m-%dT%H:%M'))
            db.session.add(new_event)
            db.session.commit()

            date_only = event_date.split('T')[0]
            time = event_date.split('T')[1]
            datetime_str = date_only + ' ' + time
            event_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')

            if submit_type == 'random':
                today = datetime.today()
                user_date = datetime.strptime(date_only, '%Y-%m-%d')

                days_between = (user_date - today).days
                if days_between > 0:
                    random_days = randrange(days_between + 1)
                    random_date = today + timedelta(days=random_days)

                    date_only = random_date.strftime('%Y-%m-%d')

            if date_only not in events:
                events[date_only] = []

            events[date_only].append((event_time, event))

        elif form_id == 'delete_event':
            event_date = request.form.get('eventDate')
            event = request.form.get('event')
            print(event_date, event)
            if event_date in events:
                events[event_date] = [e for e in events[event_date] if e[1] != event]
                if not events[event_date]:
                    del events[event_date]

    for date_only in events:
        events[date_only].sort(key=lambda x: x[0])

    this_month = calendar.month_abbr[date.month]
    return render_template('Calendar.html', this_month=this_month, date=date, content=calc_calender(date), events=events, user=current_user)
