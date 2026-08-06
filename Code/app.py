import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from bs4 import BeautifulSoup
import requests 

from helper import get_wikipedia_page, clean_page, random_page, normalize


#db = SQL("sqlite:///Wiki.db")

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    start = random_page()
    target = random_page()
    session["start"] = start
    session["target"] = target
    session["clicks"] = 0
    session["user_route"] = [start]
    return render_template("index.html", start=start, target=target)

@app.route("/play")
def play():
    start = session.get("start")
    target = session.get("target")

    if "user_route" not in session:
        return redirect('/')

    title = request.args.get("title")
    if not title:
        return redirect('/')

    normalized_title = normalize(title)
    normalized_target = normalize(target)

    if normalized_title == normalized_target:

        session["user_route"].append(normalized_title)
        session["clicks"] = session.get("clicks", 0) + 1
        return render_template("won.html")

    wikititle, content = get_wikipedia_page(title)
    if not content:
        return "Page not found!", 404
    
    cleaned_content = clean_page(content)

    if session["user_route"] and session["user_route"][-1] != title:
        session["user_route"].append(title)
        session["clicks"] = session.get("clicks", 0) + 1

    return render_template("page.html", content=cleaned_content, title=wikititle, target=target, start=start)


