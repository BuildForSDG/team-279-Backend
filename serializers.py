from flask_restful import fields

"""Defining how resources are represented
"""

tender_serializer = {
    "tender_id": fields.String,
    "tenderNumber": fields.String,
    "tenderDescription": fields.String,
    "category": fields.String,
    "datePublished": fields.String,
    "closingDate": fields.String,
    "tenderStatus": fields.String,
    "nameOfInstitution": fields.String,
    "officalLocation": fields.String,
    "InstitutionContactPerson": fields.String,
    "InstitutionPersonEmail": fields.String,
    "InstitutionPersonPhone": fields.String,
    "companyName": fields.String,
    "companyRegistrationNo": fields.String,
    "directors": fields.String,
    "cellNumber": fields.String,
    "companyAddress": fields.String,
    "awardedPoint": fields.String
}

