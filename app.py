import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from bs4 import BeautifulSoup
import requests 
import json
import shutil

from helper import get_wikipedia_page, clean_page, random_page, normalize


# Vercel doesn't support my database so I have to put it in tmp folder if I run on vercel
if os.environ.get("VERCEL"):
    db_path = "/tmp/records.db"
    if not os.path.exists(db_path) and os.path.exists("records.db"):
        shutil.copyfile("records.db", db_path)
    db = SQL(f"sqlite:///{db_path}")
else:
    # For development on Windows
    db = SQL("sqlite:///records.db")

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'local-development-fallback-key')


@app.route('/') #this is index: It gets random pages and resets counters
def index():
    if not session.get("name"):
        return redirect("/login")
    start = random_page()
    target = random_page()
    if start == target:
        target = random_page()
    session["start"] = start #session is used to store every user stats
    session["target"] = target
    session["clicks"] = 0
    session["user_route"] = [start]
    session["id"] = 0
    return render_template("index.html", start=start, target=target, name=session["name"])

@app.route("/play") #this is play: loads in page everytime and checks win condition
def play():
    start = session.get("start")
    target = session.get("target")

    if "name" not in session:
        return redirect('/login')

    title = request.args.get("title")
    if not title:
        return redirect('/')

    normalized_title = normalize(title)
    normalized_target = normalize(target)

    if session["user_route"] and session["user_route"][-1] != title:
        session["user_route"].append(normalized_title)
        session["clicks"] = session.get("clicks", 0) + 1

    if normalized_title == normalized_target: #win condition check
        #saving game to database
        path = json.dumps(session["user_route"])
        db.execute("INSERT INTO history (name, start_page, end_page, player_clicks, player_path) VALUES (?, ?, ?, ?, ?)", session["name"], start, target, session["clicks"], path)
        return render_template("won.html", name=session["name"], start=start, target=normalized_target, clicks=session["clicks"], paths=session["user_route"])

    result = get_wikipedia_page(title)
    if not result or not result[1]:
        return "Page not found!", 404

    wikititle, content = result
    if not content:
        return "Page not found!", 404
    
    cleaned_content = clean_page(content)

    return render_template("page.html", content=cleaned_content, title=wikititle, target=target, start=start)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        session["name"] = request.form.get("name")
        return redirect("/")
    else: 
        return render_template("login.html")

@app.route("/logout")
def logout():
    session["name"] = None
    return redirect("/")

@app.route("/history") #For admin only
def history():
    database = db.execute("SELECT * FROM history")
    return render_template("history.html", database=database)