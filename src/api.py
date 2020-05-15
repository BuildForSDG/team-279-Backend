from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
from app import db,ma



# Tender Clash/Model
class Tender(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tenderNumber = db.Column(db.String(25), unique=True)
    tenderDescription = db.Column(db.String(80), unique=True)
    category = db.Column(db.String(40), unique=True)
    datePublished = db.Column(db.String(15), unique=True)
    closingDate = db.Column(db.String(15), unique=True)
    tenderStatus = db.Column(db.String(10))
    nameOfInstitution = db.Column(db.String(25), unique=True)
    officalLocation = db.Column(db.String(25), unique=True)
    InstitutionContactPerson = db.Column(db.String(25))
    InstitutionPersonEmail = db.Column(db.String(25))
    InstitutionPersonPhone = db.Column(db.String(15))
    companyName =  db.Column(db.String(40), unique=True)
    companyRegistrationNo = db.Column(db.String(30), unique=True)
    directors = db.Column(db.String(50), unique=True)
    cellNumber = db.Column(db.String(15))
    companyAddress = db.Column(db.String(50), unique=True)
    awardedPoint = db.Column(db.String(10))

    def __init__(self, tenderNumber, tenderDescription, category, datePublished, closingDate, tenderStatus, nameOfInstitution, officalLocation, InstitutionContactPerson, InstitutionPersonEmail, InstitutionPersonPhone, companyName, companyRegistrationNo, directors, cellNumber, companyAddress, awardedPoint):
        self.tenderNumber = tenderNumber
        self.tenderDescription = tenderDescription
        self.category = category
        self.datePublished =datePublished
        self.closingDate = closingDate
        self.tenderStatus = tenderStatus
        self.nameOfInstitution = nameOfInstitution
        self.officalLocation = officalLocation
        self.InstitutionContactPerson = InstitutionContactPerson
        self.InstitutionPersonEmail = InstitutionPersonEmail
        self.InstitutionPersonPhone = InstitutionPersonPhone
        self.companyName = companyName
        self.companyRegistrationNo = companyRegistrationNo
        self.directors = directors
        self.cellNumber = cellNumber
        self.companyAddress = companyAddress
        self.awardedPoint = awardedPoint

# Tender schema        
class TenderSchema(ma.Schema):
    class Meta:
        fields = ('id', 'tenderNumber', 'tenderDescription', 'category', 'datePublished', 'closingDate', 'tenderStatus', 'nameOfInstitution', 'officalLocation', 'InstitutionContactPerson', 'InstitutionPersonEmail', 'InstitutionPersonPhone', 'companyName', 'companyRegistrationNo', 'directors', 'cellNumber', 'companyAddress', 'awardedPoint')

# init schema
tender_schema = TenderSchema()        
tenders_schema = TenderSchema(many=True)

# Create a Tender
@app.route('/tender', methods=['POST'])
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
    companyName =  request.json['companyName']
    companyRegistrationNo = request.json['companyRegistrationNo']
    directors = request.json['directors']
    cellNumber = request.json['cellNumber']
    companyAddress = request.json['companyAddress']
    awardedPoint = request.json['awardedPoint']

    new_tender = Tender(tenderNumber, tenderDescription, category, datePublished, closingDate, tenderStatus, nameOfInstitution, officalLocation, InstitutionContactPerson, InstitutionPersonEmail, InstitutionPersonPhone, companyName, companyRegistrationNo, directors, cellNumber, companyAddress, awardedPoint)

    db.session.add(new_tender)
    db.session.commit()

    return tender_schema.jsonify(new_tender)

# Get All products    
@app.route('/tenders', methods=['GET'])
def get_tenders():
    all_tenders = Tender.query.all()
    result = tenders_schema.dump(all_tenders)
    return jsonify(result)


""" Get Single Product by ID
@app.route('/tenders/<id>', methods=['GET'])
def get_tender(id):
    tender = Tender.query.get(id)
    return tender_schema.jsonify(tender)"""

# Update Product
@app.route('/tenders/<id>', methods=['PUT'])
def update_tender(id):
    tender = Tender.query.get(id)
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
    companyName =  request.json['companyName']
    companyRegistrationNo = request.json['companyRegistrationNo']
    directors = request.json['directors']
    cellNumber = request.json['cellNumber']
    companyAddress = request.json['companyAddress']
    awardedPoint = request.json['awardedPoint']

    tender.tenderNumber = tenderNumber
    tender.tenderDescription = tenderDescription
    tender.category = category
    tender.datePublished =datePublished
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
@app.route('/tenders/<id>', methods=['DELETE'])
def delete_tender(id):
    tender = Tender.query.get(id)
    db.session.delete(tender)
    db.session.commit()

    return tender_schema.jsonify(tender)  


# Get Tender by Tender Number    
@app.route('/api/tender/<tenderNumber>',  methods=['GET'])
def get_tender(tenderNumber):
    tender = Tender.query.filter_by(tenderNumber=tenderNumber).first_or_404()
    return tender_schema.jsonify(tender)
