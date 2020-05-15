import random

from flask import request
from flask_restful import Resource, reqparse, marshal

from src.resources import create_or_update_resource, delete_resource
from src.models import Tender
from src.serializers import tender_serializer


class TenderListAPI(Resource):
    """View all tenders; add new tender
    URL: /api/v1/tenders
    Request methods: POST, GET
    """

    def get(self):
        tenders = Tender.query.all()
        output = {"tenders": marshal(tenders, tender_serializer)}
        if tenders:
            return output
        else:
            return {"error": "There are no registered tenders. "}, 404

    @property
    def post(self):
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
        tender = Tender(tenderNumber, tenderDescription, category, datePublished, closingDate, tenderStatus,
                        nameOfInstitution, officalLocation, InstitutionContactPerson, InstitutionPersonEmail,
                        InstitutionPersonPhone, companyName, companyRegistrationNo, directors, cellNumber,
                        companyAddress, awardedPoint)

        return create_or_update_resource(resource=tender, resource_type="tender", serializer=tender_serializer,
                                         create=True)


class TendersAPI(Resource):
    """View, update and delete a single student.
    URL: /api/v1/tenders/<id>
    Request methods: GET, PUT, DELETE
    """

    def get(self, id):

        tender = Tender.query.filter_by(tender_id=id).first()
        if tender:
            return marshal(tender, tender_serializer)
        else:
            return {"error": "A tender with ID " + id + " does not exist."}, 404

    def put(self, id):

        tender = Tender.query.filter_by(student_id=id).first()
        if tender:
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
        else:
            return {"error": "A tender with ID " + id + " does not exist."}, 404

        return create_or_update_resource(resource=tender, resource_type="tender", serializer=tender_serializer,
                                         create=False)

    def delete(self, id):

        tender = Tender.query.filter_by(tender_id=id).first()
        if tender:
            return delete_resource(resource=tender, resource_type="tender", id=id)
        else:
            return {"error": "A tender with ID " + id + " does not exist."}, 404
