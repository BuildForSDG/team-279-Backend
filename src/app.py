from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os
from src.config import app_config
from flask import Flask, request, jsonify
from flask_login import LoginManager


app = Flask(__name__)
app.config.from_object(app_config[os.getenv('ENVIRONMENT')])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# init db
db.init_app(app)

from src.models import Tender

# init ma
ma = Marshmallow(app)


if os.getenv("ENVIRONMENT") == "development":
    path = "http://127.0.0.1:5000"
else:
    path = "https://team-279-Backend-develop.herokuapp.com"


# Tender schema
class TenderSchema(ma.Schema):

    """
    Tender schema field.
    """
    class Meta:
        """
        Inheritance.
        """
        fields = ('tender_id', 'tenderNumber', 'tenderDescription', 'category', 'datePublished', 'closingDate', 'tenderStatus',
                  'nameOfInstitution', 'officalLocation', 'InstitutionContactPerson', 'InstitutionPersonEmail',
                  'InstitutionPersonPhone', 'companyName', 'companyRegistrationNo', 'directors', 'cellNumber',
                  'companyAddress', 'awardedPoint')


# init schema
tender_schema = TenderSchema()
tenders_schema = TenderSchema(many=True)


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

    """
    add new tender
    URL: /api/v1/tenders
    Request methods: POST
    """
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
        companyName = request.json['companyName']
        companyRegistrationNo = request.json['companyRegistrationNo']
        directors = request.json['directors']
        cellNumber = request.json['cellNumber']
        companyAddress = request.json['companyAddress']
        awardedPoint = request.json['awardedPoint']

        new_tender = Tender(tenderNumber, tenderDescription, category, datePublished, closingDate, tenderStatus,
                            nameOfInstitution, officalLocation, InstitutionContactPerson, InstitutionPersonEmail,
                            InstitutionPersonPhone, companyName, companyRegistrationNo, directors, cellNumber,
                            companyAddress, awardedPoint)

        db.session.add(new_tender)
        db.session.commit()

        return tender_schema.jsonify(new_tender)
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
        companyName = request.json['companyName']
        companyRegistrationNo = request.json['companyRegistrationNo']
        directors = request.json['directors']
        cellNumber = request.json['cellNumber']
        companyAddress = request.json['companyAddress']
        awardedPoint = request.json['awardedPoint']

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
        tender.companyName = companyName
        tender.companyRegistrationNo = companyRegistrationNo
        tender.directors = directors
        tender.cellNumber = cellNumber
        tender.companyAddress = companyAddress
        tender.awardedPoint = awardedPoint

        db.session.commit()

        return tender_schema.jsonify(tender)
    else:
        return {"error": "A tender with ID " + tender_id + " does not exist."}, 404


# Delete Product
@app.route('/api/v1/tenders/<tender_id>', methods=['DELETE'])
def delete_tender(tender_id):

    """
    delete a single tender.
    URL: /api/v1/tenders/<tender_id>.
    Request methods: DELETE.
    """
    tender = Tender.query.get(tender_id)
    if tender:
        db.session.delete(tender)
        db.session.commit()
        return tender_schema.jsonify(tender)
    else:
        return {"error": "A tender with ID " + tender_id + " does not exist."}, 404


# Get Tender by Tender Number
# we should make the tender number cases sensitive
# deployment on heroku: Flask deployment
@app.route('/api/v1/tenders/<tenderNumber>', methods=['GET'])
def get_tender(tenderNumber):
    tender = Tender.query.filter_by(tenderNumber=tenderNumber).first_or_404()
    if tender:
        return tender_schema.jsonify(tender)
    else:
        return {"error": "A tender with ID " + tenderNumber + " does not exist."}, 404