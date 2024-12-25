from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user, login_required
from .models import User
from . import db
from datetime import datetime
import os, sys, re

views = Blueprint("views", __name__)
RECOMMENDED_ITEMS = ["推薦項目一", "推薦項目二", "推薦項目三"]

@views.route("/")
@views.route("/home")
def home():
    return render_template("home.html", user=current_user)

@views.route("/search", methods=["GET", "POST"])
@login_required
def search():
    if request.method == "POST":
        keyword = request.form.get("keyword", "").strip()

        # 檢查是否全為字母或全為數字
        if re.match("^[a-zA-Z0-9]+$", keyword):
            flash("請重輸入關鍵字，不能只包含英文或數字！", category="error")
            return render_template("search.html", user=current_user, recommendations=RECOMMENDED_ITEMS)

        # 合法輸入（包含中文）
        # flash(f"搜尋結果將顯示與 '{keyword}' 相關的內容。", category="success")
        return render_template("search.html", user=current_user, keyword=keyword, recommendations=None)

    return render_template("search.html", user=current_user, recommendations=None)