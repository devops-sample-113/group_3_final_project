from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import User
from . import db
from datetime import datetime
import os, sys, re,random
from googleapiclient.discovery import build


views = Blueprint("views", __name__)
RECOMMENDED_ITEMS = ["推薦項目一", "推薦項目二", "推薦項目三"]

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
    results = None

    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()

        # 檢查是否輸入有效文字
        if not keyword:
            flash("請輸入關鍵字！", category="error")
        elif re.match("^[a-zA-Z0-9]+$", keyword):
            flash("請重新輸入關鍵字！", category="error")
            keywords = ["舒壓活動","熱門休閒活動"]
            keyword = keywords[random.randint(0,1)]
            results = search_google_api(keyword)
            return render_template("search.html", user=current_user, keyword=None, results=results)
        else:
            # 調用 API 搜尋
            results = search_google_api(keyword)
            if not results:
                flash(f"未找到與 '{keyword}' 相關的結果。", category="info")

    return render_template("search.html", user=current_user, keyword=keyword, results=results)
