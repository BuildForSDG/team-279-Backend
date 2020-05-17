import json
import os
import requests
from flask import flash, redirect, render_template, request, url_for, jsonify
from flask_login import login_required, login_user, logout_user
from src.app import app, db
from src.models import Tender, User

if os.getenv("ENVIRONMENT") == "development":
    path = "http://127.0.0.1:5000"
else:
    path = "https://team-279-Backend-develop.herokuapp.com"


def create_admin_user():
    admin = User.query.filter_by(username="admin").first()
    if admin:
        db.session.delete(admin)
        db.session.commit()

    admin = User(username="admin", password="admin1234")
    db.session.add(admin)
    db.session.commit()


def get_token():
    admin = {"username": "admin",
             "password": "admin1234"}
    response = requests.post(path + "/api/v1/auth/login", data=admin)
    output = json.loads(response.text)
    token = output["token"]
    return {"Authorization": token}


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


@app.route("/site-map")
def site_map():
    links = []
    for rule in app.url_map.iter_rules():
        # Filter out rules we can't navigate to in a browser
        # and rules that require parameters
        if "GET" in rule.methods and has_no_empty_params(rule):
            url = url_for(rule.endpoint, **(rule.defaults or {}))
            links.append((url, rule.endpoint))
    # links is now a list of url, endpoint tuples
    print(links)
    return render_template('login.html', title='Login')


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        user = {"username": request.form["username"],
                "password": request.form["password"]}
        response = requests.post(path + "/api/v1/auth/login", data=user)
        output = json.loads(response.text)
        if output.get("error"):
            error = output["error"]
        else:
            admin_user_id = output.get("user_id")
            admin_user = User.query.get(int(admin_user_id))
            login_user(admin_user)
            return redirect(url_for('dashboard'))

    return render_template('login.html', title='Login', error=error)


@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    message = "Successfully logged out."
    return render_template('login.html', title='Login', message=message)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    tenders = Tender.query.all()
    return render_template('dashboard.html', title='Dashboard', tenders=tenders)