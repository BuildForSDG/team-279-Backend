from flask_restful import fields

"""Defining how resources are represented
"""

company_serializer = {"companyID": fields.Integer,
                      "tenderID": fields.Integer,
                      "companyName": fields.String,
                      "companyRegistrationNo": fields.String,
                      "directors": fields.String,
                      "companyPhoneNumber": fields.Integer,
                      "companyAddress": fields.String,
                      "applyCount": fields.Integer,
                      "winningCount": fields.Integer,
                      "awardedPoint": fields.Integer,
                      "tenderNumber": fields.String,
                      "isWinner": fields.String,
                      }


tender_serializer = {"tenderID": fields.Integer,
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
                     "companyNames": fields.String,
                     }
