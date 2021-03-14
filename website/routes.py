import json
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required
from website import app, bcrypt
from website.forms import RegistrationForm, LoginForm
from website.models import User
from website.dbCache import getDBData, addUser


@app.route("/")
def home():
    if current_user.is_authenticated:
        return render_template("dash.html")
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        users = getDBData()
        print(users)
        userFoundRow = None
        if users:
            for row in users:
                print(row.username)
                if row.username.lower() == form.username.data.lower():
                    userFoundRow = row
                    break

        if userFoundRow:
            if bcrypt.check_password_hash(userFoundRow.password, form.password.data):
                login_user(User(userFoundRow.id), remember=form.remember.data)
                return redirect(url_for("home"))
            flash("Incorrect password specified.")
        else:
            flash("The specified household nickname was not found")
    return render_template("login.html", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        users = getDBData()
        userFoundRow = None
        if users:
            for row in users:
                if row.username.lower() == form.username.data.lower():
                    userFoundRow = row
                    break

        if not userFoundRow:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
                "utf-8"
            )

            addUser(form.username.data, hashed_password)
            flash("User successfully created!")
            return redirect(url_for("login"))
        flash("The specified household nickname already exists")
    return render_template("register.html", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))
