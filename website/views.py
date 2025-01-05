from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import User,Activity
from . import db
from datetime import datetime
import os, sys, re,random,jieba
from googleapiclient.discovery import build


views = Blueprint("views", __name__)

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

@views.route("/search", methods=["GET", "POST"])
@login_required
def search():
    keyword = ""
    google_results = None  
    activity_results = []
    recommendations = []
    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()

        # 檢查是否輸入有效文字
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
