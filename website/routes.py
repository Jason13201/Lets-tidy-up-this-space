import json
from flask import render_template, url_for, request, redirect, flash
from flask_login import login_user, current_user, logout_user, login_required
from website import app, session, bcrypt
from website.forms import RegistrationForm, LoginForm
from website.models import User


users = session.execute("SELECT id FROM keyspace1.data;")
nextUserId = 1 + max([row.id for row in users]) if users else 1


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        users = session.execute("SELECT id, username, password FROM keyspace1.data;")
        userFoundRow = None
        if users:
            for row in users:
                if row.username.lower() == form.username.data:
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
        users = session.execute("SELECT id, username, password FROM keyspace1.data;")
        userFoundRow = None
        if users:
            for row in users:
                if row.username.lower() == form.username.data:
                    userFoundRow = row
                    break

        if not userFoundRow:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
                "utf-8"
            )
            session.execute(
                """
            INSERT INTO keyspace1.data (id, username, password, misc)
            VALUES (%s, %s, %s, %s)
            """,
                (nextUserId, form.username.data, hashed_password, "{}"),
            )
            flash("User successfully created!")
            return redirect(url_for("login"))
        flash("The specified household nickname already exists")
    return render_template("register.html", form=form)
