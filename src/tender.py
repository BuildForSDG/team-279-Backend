from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os
from sqlalchemy import engine
from src.config import app_config
from flask import Flask, request, jsonify, abort
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from sqlalchemy.orm import sessionmaker


Session = sessionmaker(bind=engine)
session = Session()

app = Flask(__name__)
app.config.from_object(app_config[os.getenv('ENVIRONMENT')])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)

# after the db variable initialization
login_manager = LoginManager()
Bootstrap(app)
login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.login"

# init db
db.init_app(app)

from src.models import Tender, Company, TenderSchema, CompanySchema
# imported each blueprint object and registered it
# from src.admin import admin as admin_blueprint
# app.register_blueprint(admin_blueprint, url_prefix='/admin')
from src.auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)
from src.home import home as home_blueprint

app.register_blueprint(home_blueprint)

if os.getenv("ENVIRONMENT") == "development":
    path = "http://127.0.0.1:5000"
else:
    path = "https://team-279-Backend-develop.herokuapp.com"

# init schema
tender_schema = TenderSchema()
tenders_schema = TenderSchema(many=True)


@app.route('/api/v1/display_tender/<tenderNumber>', methods=['POST'])
def display_tender(tenderNumber):
    companyName = request.json['companyName']
    directors = request.json['directors']
    companyRegistrationNo = request.json['companyRegistrationNo']
    company_phone_number = request.json['company_phone_number']
    companyAddress = request.json['companyAddress']
    apply_count = request.json['apply_count']
    winning_count = request.json['winning_count']
    awardedPoint = request.json['awardedPoint']

    new_company = Company(companyName, directors, companyRegistrationNo, company_phone_number,
                          companyAddress, apply_count, winning_count, awardedPoint)
    company_names_dict = company_schema.dump(new_company)

    db.session.add(Tender)
    db.session.commit()







    # company_names_dict['company_names'] = []
    tender_list = Tender.query.filter_by(tenderNumber=tenderNumber)
    # tender = Tender.query.get(tenderNumber)
    tender_list_of_dict = tender_schema.dump(tender_list)

    from collections import OrderedDict
    result = OrderedDict()

    for tender_dict in tender_list_of_dict:
        for key in list(tender_dict.keys()):
            if key in list(company_names_dict.keys()) and (str(company_names_dict['tenderNumber']) == tenderNumber):
                if company_names_dict['tender_id'] == 'null':
                    tender_id = tender_dict['tender_id']
                    company_names_dict['tender_id'] = company_names_dict['tender_id'].replace('null', str(tender_id))


    for tender_dict in tender_list_of_dict:
        for key, val in tender_dict.items():
            if key in list(company_names_dict.keys()) and (val == str(company_names_dict['tenderNumber'])):
                Tender.company_names.append(company_names_dict)
                # tender_query = db.session.query(Tender).filter_by(tenderNumber=tenderNumber)
                # tender_list_of_dict['company_names'] = company_names_dict
                # tender_list_of_dict.update(company_names=[company_names_dict])
                # tender_query.update(tender_list_of_dict)
        db.session.add(Tender)
        # Tender.update(tender_list_of_dict)
    db.session.commit()

    # db.session.add(tender_list_of_dict)
    # db.session.commit()

    return tender_schema.jsonify(tender_list_of_dict)


testing = [{
    "tenderNumber": "TENDER1096",
    "tenderDescription": "Supply of covid-19 ventilators",
    "category": "General Health Service",
    "datePublished": "14/05/2020",
    "closingDate": "23/06/2020",
    "tenderStatus": "open",
    "nameOfInstitution": "Dep of labour",
    "officalLocation": "101 Bellair road",
    "InstitutionContactPerson": "",
    "InstitutionPersonEmail": "ola@sample.co.za",
    "InstitutionPersonPhone": "0117478850",
    "global_apply_count": " ",
    "global_winning_count": " "
}
]


#
#
#
# @app.route('/api/v1/companies/<tenderNumber>', methods=['POST'])
# def add_companies(tenderNumber):
#
#     if request.method == 'POST':
#         companyName = request.json['companyName']
#         directors = request.json['directors']
#         companyRegistrationNo = request.json['companyRegistrationNo']
#         company_phone_number = request.json['company_phone_number']
#         companyAddress = request.json['companyAddress']
#         apply_count = request.json['apply_count']
#         winning_count = request.json['winning_count']
#         awardedPoint = request.json['awardedPoint']
#         # tenderNumber = tenderNumber
#
#         new_companies = Company(companyName, directors, companyRegistrationNo, company_phone_number,
#                                 companyAddress, apply_count, winning_count, awardedPoint, tenderNumber)
#
#
#         # tender_schema = TenderSchema()
#         tenders_schema = TenderSchema(many=True)
#         tender_list = Tender.query.filter_by(tenderNumber=tenderNumber)
#         # tender = Tender.query.get(tenderNumber)
#         tender_list_of_dict = tenders_schema.dump(tender_list)
#
#         company_names_dict = company_schema.dump(new_companies)
#         for tender_dict in tender_list_of_dict:
#             for key in list(tender_dict.keys()):
#                 if key in list(company_names_dict.keys()) and (str(company_names_dict['tenderNumber']) == str(tenderNumber)):
#                     if company_names_dict['tender_id'] == 'null':
#                         tender_id = tender_dict['tender_id']
#                         company_names_dict['tender_id'] = company_names_dict['tender_id'].replace('null',str(tender_id))
#                         tender_dict['company_names'] = new_companies
#                         db.session.add(tender_dict['company_names'])
#
#
#         db.session.add(new_companies)
#         db.session.commit()
#
#         return str(new_companies)
#     else:
#         return {"error": "Specified tender doesn't exit!"}, 404
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#


# Get one tender
@app.route('/api/v1/tender/<tender_id>', methods=['GET'])
def get_one_tender(tender_id):
    """
    This function responds to a request for /api/vi/tender/<tender_id>
    with one matching tender from companies
    :param tender_id:   Id of tender to find
    :return:            tender matching id
    """
    # Build the initial query
    tender = (Tender.query.filter(Tender.tender_id == tender_id).outerjoin(Company).one_or_none())
    # Did we find a tender?
    if tender is not None:
        # Serialize the data for the response
        data = tender_schema.dump(tender)
        return jsonify(data)
    # Otherwise, nope, didn't find that tender
    else:
        abort(404, "Tender not found for Id: {}".format(tender_id))


# Get one company
@app.route('/api/v1/company/<company_id>', methods=['GET'])
def get_one_company(company_id):
    """
    This function responds to a request for /api/vi/company/<company_id>
    with one matching company from companies
    :param company_id:   Id of company to find
    :return:            company matching id
    """
    # Build the initial query
    company = (Company.query.filter(Company.company_id == company_id).outerjoin(Tender).one_or_none())
    # Did we find a company?
    if company is not None:
        # Serialize the data for the response
        company_schema = CompanySchema()
        data = company_schema.dump(company)
        return jsonify(data)
    # Otherwise, nope, didn't find that company
    else:
        abort(404, "Company not found for Id: {}".format(company_id))


@app.route('/api/v1/tender/<tender_id>/company/<company_id>', methods=['GET'])
def read_one(tender_id, company_id):
    """
    This function responds to a request for
    /api/v1/tender/{tender_id}/companies/{company_id}
    with one matching company for the associated tender

    :param tender_id:       Id of tender the company is related to
    :param company_id:         Id of the company
    :return:                json string of company contents
    """
    # Query the database for the company
    company = (
        Company.query.join(Tender, Tender.tender_id == Company.tender_id).filter(Tender.tender_id == tender_id).filter(
            Company.company_id == company_id).all())

    # company = (Tender.query.join(Company, Company.tender_id == Tender.tender_id).filter(Company.tender_id == tender_id).filter(Tender.company_id == company_id).one_or_none())

    # company = db.session.query(Company, Tender).filter(Company.company_id == Tender.tender_id).all()
    # Was a company found?
    if company is not None:
        data = company_schema.dump(company)
        return jsonify(data)

    # Otherwise, nope, didn't find that note
    else:
        abort(404, "Company not found for Id: {}".format(company_id))


# Get All products
@app.route('/api/v1/tenders', methods=['GET'])
def get_tenders():
    """
    View all tenders
    URL: /api/v1/tenders
    Request methods: GET
    """
    all_tenders = Tender.query.all()
    result = tenders_schema.dump(all_tenders)
    return jsonify(result)


# Create a Tender
@app.route('/api/v1/tenders', methods=['POST'])
def add_tender():
    if request.method == 'POST':
        tenderNumber = request.json['tenderNumber']
        tenderDescription = request.json['tenderDescription']
        category = request.json['category']
        datePublished = request.json['datePublished']
        closingDate = request.json['closingDate']
        tenderStatus = request.json['tenderStatus']
        nameOfInstitution = request.json['nameOfInstitution']
        officalLocation = request.json['officalLocation']
        InstitutionContactPerson = request.json['InstitutionContactPerson']
        InstitutionPersonEmail = request.json['InstitutionPersonEmail']
        InstitutionPersonPhone = request.json['InstitutionPersonPhone']
        global_apply_count = request.json['global_apply_count']
        global_winning_count = request.json['global_winning_count']
        company_names = request.json['global_winning_count']


        new_tender = Tender(tenderNumber, tenderDescription, category, datePublished, closingDate, tenderStatus,
                            nameOfInstitution, officalLocation, InstitutionContactPerson, InstitutionPersonEmail,
                            InstitutionPersonPhone, global_apply_count, global_winning_count, company_names)

        db.session.add(new_tender)
        db.session.commit()

        return str(new_tender)
    else:
        return {"error": "Specified tender doesn't exit!"}, 404


# Update Product
@app.route('/api/v1/tenders/<tender_id>', methods=['PUT'])
def update_tender(tender_id):
    """
    update a single tender.
    URL: /api/v1/tenders/<tender_id>
    Request methods: PUT
    """
    tender = Tender.query.get(tender_id)
    if tender:
        tenderNumber = request.json['tenderNumber']
        tenderDescription = request.json['tenderDescription']
        category = request.json['category']
        datePublished = request.json['datePublished']
        closingDate = request.json['closingDate']
        tenderStatus = request.json['tenderStatus']
        nameOfInstitution = request.json['nameOfInstitution']
        officalLocation = request.json['officalLocation']
        InstitutionContactPerson = request.json['InstitutionContactPerson']
        InstitutionPersonEmail = request.json['InstitutionPersonEmail']
        InstitutionPersonPhone = request.json['InstitutionPersonPhone']
        company_names = request.json['company_names']
        global_apply_count = request.json['global_apply_count']
        global_winning_count = request.json['global_winning_count']

        tender.tenderNumber = tenderNumber
        tender.tenderDescription = tenderDescription
        tender.category = category
        tender.datePublished = datePublished
        tender.closingDate = closingDate
        tender.tenderStatus = tenderStatus
        tender.nameOfInstitution = nameOfInstitution
        tender.officalLocation = officalLocation
        tender.InstitutionContactPerson = InstitutionContactPerson
        tender.InstitutionPersonEmail = InstitutionPersonEmail
        tender.InstitutionPersonPhone = InstitutionPersonPhone
        tender.company_names = company_names
        tender.global_apply_count = global_apply_count
        tender.global_winning_count = global_winning_count

        db.session.commit()

        return tender_schema.jsonify(tender)
    else:
        return {"error": "A tender with ID " + tender_id + " does not exist."}, 404


# Delete Product
@app.route('/api/v1/tenders/<tender_id>', methods=['DELETE'])
def delete_tender(tender_id):
    """
    delete a single tender.
    URL: /api/v1/tenders/<tender_id>
    Request methods: DELETE
    pydocstyle - -ignore = D101, D213
    """
    tender = Tender.query.get(tender_id)
    if tender:
        db.session.delete(tender)
        db.session.commit()
        return tender_schema.jsonify(tender)
    else:
        return {"error": "A tender with ID " + tender_id + " does not exist."}, 404


@app.route('/api/v1/tenders/<tenderNumber>/', methods=['GET'])
def get_tender(tenderNumber):
    tender = Tender.query.filter_by(tenderNumber=tenderNumber)

    if tender:
        return tenders_schema.jsonify(tender)
    else:
        return {"error": "A tender with ID " + tenderNumber + " does not exist."}, 404


# init schema
company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)

companyheader = {
    "companyName": "Ola",
    "directors": "Olu",
    "companyRegistrationNo": "FND/2323",
    "company_phone_number": "+27791024568",
    "companyAddress": "Cape town",
    "apply_count": "1",
    "winning_count": "0",
    "awardedPoint": " ",
    "tenderNumber": "TENDER1095",
    "bid_tender_number": "TENDER1095"
}


@app.route('/api/v1/post_company/<tenderNumber>', methods=['POST'])
def post_company(tenderNumber):
    if request.method == 'POST':

        companyName = request.json['companyName']
        directors = request.json['directors']
        companyRegistrationNo = request.json['companyRegistrationNo']
        company_phone_number = request.json['company_phone_number']
        companyAddress = request.json['companyAddress']
        apply_count = request.json['apply_count']
        winning_count = request.json['winning_count']
        awardedPoint = request.json['awardedPoint']

        new_company = Company(companyName, directors, companyRegistrationNo, company_phone_number,
                              companyAddress, apply_count, winning_count, awardedPoint, tenderNumber)
        db.session.add(new_company)
        db.session.commit()

        return str(new_company)
    else:
        return {"error": "Specified tender doesn't exit!"}, 404



# Get All products
@app.route('/api/v1/companies', methods=['GET'])
def get_company():
    """
    View all companies
    URL: /api/v1/companies
    Request methods: GET
    """
    all_companies = Company.query.all()
    company_result = companies_schema.dump(all_companies)
    return jsonify(company_result)


# # Get one company
# @app.route('/api/v1/company/<company_id>', methods=['GET'])
# def get_one_company(company_id):
#     """
#     This function responds to a request for /api/vi/company/<company_id>
#     with one matching company from companies
#     :param company_id:   Id of company to find
#     :return:            company matching id
#     """
#     # Build the initial query
#     company = (Company.query.filter(Company.company_id == company_id).outerjoin(Tender).one_or_none())
#     # Did we find a company?
#     if company is not None:
#         # Serialize the data for the response
#         data = company_schema.dump(company)
#         return jsonify(data)
#     # Otherwise, nope, didn't find that company
#     else:
#         abort(404, "Company not found for Id: {}".format(company_id))
# #
# #
#
# @app.route('/api/v1/tender/<tender_id>/company/<company_id>', methods=['GET'])
# def read_one(tender_id, company_id):
#     """
#     This function responds to a request for
#     /api/v1/tender/{tender_id}/companies/{company_id}
#     with one matching company for the associated tender
#
#     :param tender_id:       Id of tender the company is related to
#     :param company_id:         Id of the company
#     :return:                json string of company contents
#     """
#     # Query the database for the company
#     company = (
#         Company.query.join(Tender, Tender.tender_id == Company.tender_id).filter(Tender.tender_id == tender_id).filter(
#             Company.company_id == company_id).all())
#
#     # company = (Tender.query.join(Company, Company.tender_id == Tender.tender_id).filter(Company.tender_id == tender_id).filter(Tender.company_id == company_id).one_or_none())
#     # company = db.session.query(Company, Tender).filter(Company.company_id == Tender.tender_id).all()
#     # Was a company found?
#     if company is not None:
#         data = company_schema.dump(company)
#         return jsonify(data)
#
#     # Otherwise, nope, didn't find that note
#     else:
#         abort(404, "Company not found for Id: {}".format(company_id))


@app.route('/api/v1/displayCompany/<tenderNumber>', methods=['GET'])
def display_company(tenderNumber):
    if request.method == 'GET':
        company_query = Company.query.filter_by(tenderNumber=tenderNumber)
        company_list_dictionary = companies_schema.dump(company_query)
        tender_client = db.session.query(Tender).filter_by(tenderNumber=tenderNumber)
        tender_list_of_dict = tenders_schema.dump(tender_client)
        for tender_dict in tender_list_of_dict:
            for key in list(tender_dict.keys()):
                for company_names_dict in company_list_dictionary:
                    if key in list(company_names_dict.keys()):
                        if company_names_dict['tender_id'] is None:
                            company_names_dict['tender_id'] = tender_dict['tender_id']
                            db.session.commit()
                            for row in Tender.query.filter_by(tenderNumber=tenderNumber):
                                row.company_names = company_list_dictionary
                            db.session.commit()
        tender_client = db.session.query(Tender).filter_by(tenderNumber=tenderNumber)
        tenders = tenders_schema.dump(tender_client)
        if tender_client:
            return jsonify(tenders)
        else:
            return {"error": "A tender with ID " + tenderNumber + " does not exist."}, 404
    else:
        return {"error": "Specified tender doesn't exit!"}, 404


@app.route('/api/v1/edit-company/<tenderNumber>', methods=['PUT'])
def edit_company(tenderNumber):
    company = Company.query.filter_by(tenderNumber=tenderNumber).first()

    if request.method == 'PUT':
        companyName = request.json['companyName']
        directors = request.json['directors']
        companyRegistrationNo = request.json['companyRegistrationNo']
        company_phone_number = request.json['company_phone_number']
        companyAddress = request.json['companyAddress']
        apply_count = request.json['apply_count']
        winning_count = request.json['winning_count']
        awardedPoint = request.json['awardedPoint']

        company.companyName = companyName
        company.companyRegistrationNo = companyRegistrationNo
        company.directors = directors
        company.company_phone_number = company_phone_number
        company.companyAddress = companyAddress
        company.apply_count = apply_count
        company.winning_count = winning_count
        company.awardedPoint = awardedPoint

        db.session.commit()

        return company_schema.jsonify(company)
    else:
        return {"error": "A company with tenderNumber " + tenderNumber + " does not exist."}, 404


@app.route('/api/v1/delete-company/<tenderNumber>/<company_id>', methods=['DELETE'])
def delete_company(tenderNumber, company_id):
    # company = Company.query.filter_by(tenderNumber=tenderNumber).first()
    company = (Company.query.join(Tender, Tender.tenderNumber == Company.tenderNumber).filter(Company.company_id == company_id).all())
    if request.method == 'DELETE':
        db.session.delete(company)
        db.session.commit()
        return company_schema.jsonify(company)
    else:
        return {"error": "A company with tenderNumber " + tenderNumber + " does not exist."}, 404
