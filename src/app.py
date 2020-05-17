from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
import os
from src.config import app_config
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config.from_object(app_config[os.getenv('ENVIRONMENT')])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# init db
db = SQLAlchemy(app)
db.init_app(app)

from src.models import Tender

# init ma
ma = Marshmallow(app)


# Tender schema
class TenderSchema(ma.Schema):

    """
    Tender schema field.
    """

    class Meta:

        """
        Inheritance.
        """

        fields = ('id', 'tenderNumber', 'tenderDescription', 'category', 'datePublished', 'closingDate', 'tenderStatus',
                  'nameOfInstitution', 'officalLocation', 'InstitutionContactPerson', 'InstitutionPersonEmail',
                  'InstitutionPersonPhone', 'companyName', 'companyRegistrationNo', 'directors', 'cellNumber',
                  'companyAddress', 'awardedPoint')


# init schema
tender_schema = TenderSchema()
tenders_schema = TenderSchema(many=True)


# Get All products
@app.route('/api/tenders', methods=['GET'])
def get_tenders():
    all_tenders = Tender.query.all()
    result = tenders_schema.dump(all_tenders)
    return jsonify(result)


# Create a Tender
@app.route('/api/tenders', methods=['POST'])
def add_tender():
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


# Update Product
@app.route('/api/tenders/<tender_id>', methods=['PUT'])
def update_tender(tender_id):
    tender = Tender.query.get(tender_id)
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


# Delete Product
@app.route('/api/tenders/<tender_id>', methods=['DELETE'])
def delete_tender(tender_id):
    tender = Tender.query.get(tender_id)
    db.session.delete(tender)
    db.session.commit()

    return tender_schema.jsonify(tender)


# Get Tender by Tender Number
# we should make the tender number cases sensitive
# deployment on heroku: Flask deployment
@app.route('/api/tenders/<tenderNumber>', methods=['GET'])
def get_tender(tenderNumber):
    tender = Tender.query.filter_by(tenderNumber=tenderNumber).first_or_404()
    return tender_schema.jsonify(tender)
