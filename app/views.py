import json
import os
import requests
from app import app, db
from flask import flash, redirect, render_template, request, url_for, jsonify, Blueprint
from flask_login import login_required, login_user, logout_user
from app.models import Tender, TenderSchema, Company, CompanySchema, User


if os.getenv("ENVIRONMENT") == "development":
    path = "http://127.0.0.1:5000"
else:
    path = "https://vtender.herokuapp.com/"

# init schema
tender_schema = TenderSchema()
tenders_schema = TenderSchema(many=True)

company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)


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
    return render_template("login.html", title='Login')


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
    company = Company.query.all()
    return render_template('dashboard.html', title='Dashboard', tenders=tenders, company=company)


@app.route('/add-tender', methods=['GET', 'POST'])
# @login_required
def add_tender():
    if request.method == 'POST':
        # create_admin_user()
        tender = {"tenderNumber": request.form["tenderNumber"],
                  "tenderDescription": request.form["tenderDescription"],
                  "category": request.form["category"],
                  "datePublished": request.form["datePublished"],
                  "closingDate": request.form["closingDate"],
                  "tenderStatus": request.form["tenderStatus"],
                  "nameOfInstitution": request.form["nameOfInstitution"],
                  "officalLocation": request.form["officalLocation"],
                  "InstitutionContactPerson": request.form["InstitutionContactPerson"],
                  "InstitutionPersonEmail": request.form["InstitutionPersonEmail"],
                  "InstitutionPersonPhone": request.form["InstitutionPersonPhone"]
                  }
        response = requests.post(path + "/api/v1/tenders", data=tender, headers=get_token())
        output = json.loads(response.text)
        if output.get("error"):
            flash(output["error"], "error")
        else:
            if "error" in output["message"].lower():
                flash(output["message"], "error")
            else:
                flash(output["message"], "success")

        return redirect(url_for('dashboard'))


@app.route('/edit-tender/<string:tenderID>', methods=['GET', 'POST'])
# @login_required
def edit_tender(tenderID):
    tender = Tender.query.filter_by(tenderID=tenderID).first()
    if tender:
        if request.method == 'POST':
            # create_admin_user()
            tender = {"tenderNumber": request.form["tenderNumber"],
                      "tenderDescription": request.form["tenderDescription"],
                      "category": request.form["category"],
                      "datePublished": request.form["datePublished"],
                      "closingDate": request.form["closingDate"],
                      "tenderStatus": request.form["tenderStatus"],
                      "nameOfInstitution": request.form["nameOfInstitution"],
                      "officalLocation": request.form["officalLocation"],
                      "InstitutionContactPerson": request.form["InstitutionContactPerson"],
                      "InstitutionPersonEmail": request.form["InstitutionPersonEmail"],
                      "InstitutionPersonPhone": request.form["InstitutionPersonPhone"]
                      }
            response = requests.put(path + "/api/v1/tenders/" + tenderID, data=tender, headers=get_token())
            output = json.loads(response.text)
            if output.get("error"):
                flash(output["error"], "error")
            else:
                if "error" in output["message"].lower():
                    flash(output["message"], "error")
                else:
                    flash(output["message"], "success")
    else:
        flash("Specified tender doesn't exit!", "error")

    return redirect(url_for('dashboard'))


@app.route('/delete-tender/<string:tenderID>', methods=['GET', 'POST'])
# @login_required
def delete_tender(tenderID):
    tender = Tender.query.filter_by(tenderID=tenderID).first()
    if tender:
        # create_admin_user()
        response = requests.delete(path + "/api/v1/tenders/" + tenderID, headers=get_token())
        output = json.loads(response.text)
        if output.get("error"):
            flash(output["error"], "error")
        else:
            if "error" in output["message"].lower():
                flash(output["message"], "error")
            else:
                flash(output["message"], "success")
    else:
        flash("Specified tender doesn't exit!", "error")

    return redirect(url_for('dashboard'))


@app.route('/add-company', methods=['GET', 'POST'])
# @login_required
def add_company():
    if request.method == 'POST':
        # create_admin_user()
        company = {"tenderNumber": request.form["tenderNumber"],
                   "companyName": request.form["companyName"],
                   "directors": request.form["directors"],
                   "companyRegistrationNo": request.form["companyRegistrationNo"],
                   "companyPhoneNumber": request.form["companyPhoneNumber"],
                   "companyAddress": request.form["companyAddress"],
                   "awardedPoint": request.form["awardedPoint"],
                   "isWinner": request.form["isWinner"]}
        response = requests.post(path + "/api/v1/company", data=company, headers=get_token())
        output = json.loads(response.text)
        if output.get("error"):
            flash(output["error"], "error")
        else:
            if "error" in output["message"]:
                flash(output["message"], "error")
            else:
                flash(output["message"], "success")

        return redirect(url_for('dashboard'))


@app.route('/edit-company/<string:companyID>', methods=['GET', 'POST'])
# @login_required
def edit_company(companyID):
    company = Company.query.filter_by(companyID=companyID).first()
    if company:
        if request.method == 'POST':
            # create_admin_user()
            company = {"tenderNumber": request.form["companyName"],
                       "companyName": request.form["companyName"],
                       "directors": request.form["directors"],
                       "companyRegistrationNo": request.form["companyRegistrationNo"],
                       "company_phone_number": request.form["company_phone_number"],
                       "companyAddress": request.form["companyAddress"],
                       "awardedPoint": request.form["awardedPoint"],
                       "isWinner": request.form["isWinner"]
                       }
            response = requests.put(path + "/api/v1/company/" + companyID, data=company, headers=get_token())
            output = json.loads(response.text)
            if output.get("error"):
                flash(output["error"], "error")
            else:
                if "error" in output["message"].lower():
                    flash(output["message"], "error")
                else:
                    flash(output["message"], "success")
    else:
        flash("Specified company doesn't exit!", "error")

    return redirect(url_for('dashboard'))


@app.route('/delete-company/<string:companyID>', methods=['GET', 'POST'])
# @login_required
def delete_company(companyID):
    company = Company.query.filter_by(companyID=companyID).first()
    if company:
        # create_admin_user()
        response = requests.delete(path + "/api/v1/company/" + companyID, headers=get_token())
        output = json.loads(response.text)
        if output.get("error"):
            flash(output["error"], "error")
        else:
            if "error" in output["message"].lower():
                flash(output["message"], "error")
            else:
                flash(output["message"], "success")
    else:
        flash("Specified company doesn't exit!", "error")

    return redirect(url_for('dashboard'))



@app.route('/combined-tenders', methods=['GET'])
# @login_required
# Get All tender application products
def get_combined_tenders():
    if request.method == 'GET':
        # create_admin_user()
        tender_client = db.session.query(Tender).filter()
        tender_records = tenders_schema.dump(tender_client)
        if tender_client:
            response = requests.get(path + "/api/v1/combined-tenders", data=tender_records, headers=get_token())
            output = json.loads(response.text)
            if output.get("error"):
                flash(output["error"], "error")
            else:
                if "error" in output["message"].lower():
                    flash(output["message"], "error")
                else:
                    flash(output["message"], "success")
    else:
        flash("Specified company doesn't exit!", "error")

    return redirect(url_for('dashboard'))


@app.route('/one-tender/<string:tenderNumber>', methods=['GET'])
# @login_required
def get_combined_tender(tenderNumber):
    if request.method == 'GET':
        # create_admin_user()
        tender_client = db.session.query(Tender).filter_by(tenderNumber=tenderNumber)
        tender_records = tenders_schema.dump(tender_client)
        if tender_client:
            response = requests.get(path + "/api/v1/one-tender/" + tenderNumber, data=tender_records,
                                    headers=get_token())
            output = json.loads(response.text)
            if output.get("error"):
                flash(output["error"], "error")
            else:
                if "error" in output["message"].lower():
                    flash(output["message"], "error")
                else:
                    flash(output["message"], "success")
    else:
        flash("Specified company doesn't exit!", "error")

    return redirect(url_for('dashboard'))
