from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import User,Activity, Event
from . import db
from datetime import datetime, timedelta
import os, sys, re,random,jieba
from googleapiclient.discovery import build

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

API_KEY = "AIzaSyCOkhpfgz_gmnyRyee-wW06MEdIPwUUoSc"  
CSE_ID = "e2b3823040bc04198"  

def search_google_api(keyword):
    """調用 Google Custom Search API 搜尋"""
    service = build("customsearch", "v1", developerKey=API_KEY)
    res = service.cse().list(q=keyword, cx=CSE_ID).execute()
    return res.get("items", [])  # 返回搜尋結果

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

            if submit_type == 'random':
                today = datetime.today()
                user_date = datetime.strptime(date_only, '%Y-%m-%d')

                days_between = (user_date - today).days
                if days_between > 0:
                    random_days = randrange(days_between + 1)
                    random_date = today + timedelta(days=random_days)

                    date_only = random_date.strftime('%Y-%m-%d')

            datetime_str = date_only + ' ' + time
            event_time = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M')
            if date_only not in events:
                events[date_only] = []

            events[date_only].append((event_time, event))
            # print(events[date_only])

        elif form_id == 'delete_event':
            event_date = request.form.get('eventDate')
            event = request.form.get('event')
            event_time = request.form.get('eventTime')
            event_time = datetime.strptime(event_time, '%Y-%m-%d %H:%M')
            # print(event_date, event, event_time)
            if event_date in events:
                # print(events[event_date])
                events[event_date] = [e for e in events[event_date] if not (e[1] == event and e[0] == event_time)]
                # print(events[event_date])
                if not events[event_date]:
                    del events[event_date]

    for date_only in events:
        events[date_only].sort(key=lambda x: x[0])

    this_month = calendar.month_abbr[date.month]
    return render_template('Calendar.html', this_month=this_month, date=date, content=calc_calender(date), events=events, user=current_user)

@views.route("/search", methods=["GET", "POST"])
@login_required
def search():
    keyword = ""
    google_results = None
    activity_results = []
    recommendations = []
    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()

        if not keyword:
            flash("請輸入關鍵字！", category="error")
        elif re.match("^[a-zA-Z0-9]+$", keyword):
            flash("無搜尋結果，請重新輸入關鍵字！", category="error")
            recommendations = Activity.query.order_by(db.func.random()).limit(5).all()
        else:
            if "音樂" in keyword:
                google_results = search_google_api(keyword)
                if not google_results:
                    flash(f"未找到與 '{keyword}' 相關的結果。", category="error")
                    recommendations = Activity.query.order_by(db.func.random()).limit(5).all()
            else:
                words = jieba.lcut(keyword)
                query = Activity.query
                conditions = []
                # 將分詞結果逐一加入查詢條件
                for word in words:
                    word = word.strip()
                    if word:
                        conditions.append(
                            db.or_(
                                Activity.name.like(f"%{word}%"),
                                Activity.description.like(f"%{word}%"),
                                Activity.tags.like(f"%{word}%")
                            )
                        )

                # 合併所有條件
                if conditions:
                    query = query.filter(db.or_(*conditions))

                activity_results = query.all()

                if not activity_results:
                    flash(f"未找到與 '{keyword}' 相關的資料庫結果。", category="error")
                    recommendations = Activity.query.order_by(db.func.random()).limit(5).all()
    return render_template("search.html", user=current_user, keyword=keyword, google_results=google_results,activity_results=activity_results,recommendations=recommendations)



@views.route("/spin_the_wheel")
def spin_the_wheel():
    return render_template("spin_the_wheel.html", user=current_user)