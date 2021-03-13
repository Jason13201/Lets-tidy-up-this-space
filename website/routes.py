import json
from flask import render_template, url_for, request, redirect
from website import app


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    return render_template("home.html")


@app.route("/register")
def register():
    return render_template("home.html")
