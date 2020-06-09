from flask_restful import fields

"""Defining how resources are represented
"""

company_serializer = {"company_id": fields.Integer,
                      "tender_id": fields.Integer,
                      "companyName": fields.String,
                      "companyRegistrationNo": fields.String,
                      "directors": fields.String,
                      "company_phone_number": fields.Integer,
                      "companyAddress": fields.String,
                      "apply_count": fields.Integer,
                      "winning_count": fields.Integer,
                      "awardedPoint": fields.Integer,
                      "tenderNumber": fields.String,
                      "is_winner": fields.Boolean(),
                      }


tender_serializer = {"tender_id": fields.Integer,
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
                     "company_names": fields.String,
                     }
