from flask import request
from flask_restful import Resource, reqparse, marshal
from app.resources import create_or_update_resource, delete_resource
from app.models import Company, TenderSchema, CompanySchema
from app.serializers import company_serializer
from sqlalchemy.event import listen
from sqlalchemy import event, DDL


# init schema
tender_schema = TenderSchema()
tenders_schema = TenderSchema(many=True)

company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)


# https://dzone.com/articles/how-to-initialize-database-with-default-values-in
@event.listens_for(Company.__table__, 'after_create')
def insert_initial_values(*args, **kwargs):
    db.session.add(Company(isWinner='notWinner'))
    db.session.commit()


event.listen(Company.__table__, 'after_create', insert_initial_values)


class CompanyListAPI(Resource):
    """View all company; add new company
    URL: /api/v1/company
    Request methods: POST, GET
    """

    def get(self):

        args = request.args.to_dict()
        page = int(args.get("page", 1))
        limit = int(args.get("limit", 20))
        kwargs = {}

        company = Company.query.filter_by(**kwargs).paginate(page=page, per_page=limit, error_out=False)
        page_count = company.pages
        has_next = company.has_next
        has_previous = company.has_prev
        if has_next:
            next_page = str(request.url_root) + "api/v1.0/company?" + \
                        "limit=" + str(limit) + "&page=" + str(page + 1)
        else:
            next_page = "None"
        if has_previous:
            previous_page = request.url_root + "api/v1.0/company?" + \
                            "limit=" + str(limit) + "&page=" + str(page - 1)
        else:
            previous_page = "None"
        company = company.items

        output = {"company": marshal(company, company_serializer),
                  "has_next": has_next,
                  "page_count": page_count,
                  "previous_page": previous_page,
                  "next_page": next_page
                  }

        if company:
            return output
        else:
            return {"error": "There are no registered company. Add a new one and try again!"}, 404


    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument("tenderNumber", help="Please enter a tender number for a company.")
        parser.add_argument("companyName", required=True, help="Please enter a company name.")
        parser.add_argument("directors", required=True, help="Please enter a directors.")
        parser.add_argument("companyRegistrationNo", required=True, help="Please enter a company registration number.")
        parser.add_argument("companyPhoneNumber", help="Enter the company phone number.")
        parser.add_argument("companyAddress", help="Enter the company address.")
        parser.add_argument("awardedPoint", required=True, help="Please enter awarded point.")
        parser.add_argument("isWinner", required=True, help="Please enter awarded point.")

        args = parser.parse_args()

        tenderNumber, companyName, directors, companyRegistrationNo, companyPhoneNumber, companyAddress, awardedPoint, isWinner = \
            args["tenderNumber"], args["companyName"], args["directors"], args["companyRegistrationNo"], \
            args["companyPhoneNumber"], args["companyAddress"], args["awardedPoint"], args["isWinner"]

        company = Company(tenderNumber=tenderNumber,
                          companyName=companyName,
                          directors=directors,
                          companyRegistrationNo=companyRegistrationNo,
                          companyPhoneNumber=companyPhoneNumber,
                          companyAddress=companyAddress,
                          awardedPoint=awardedPoint,
                          isWinner=isWinner
                          )
        # if company.apply_count == 'null' and companyRegistrationNo is not None:
        #     try:
        #         companyRegistrationNo = Company.query.get(companyRegistrationNo)
        #         if companyRegistrationNo:
        #             count += 1
        #             company.apply_count.append(count)
        #         else:
        #             return {"error": "cannot assign value to apply_count"}, 400
        #     except:
        #         return {"error": "The company already apply for this tender number"}, 400
        return create_or_update_resource(resource=company, resource_type="company", serializer=company_serializer, create=True)


class CompanyAPI(Resource):
    """View, update and delete a single company.
    URL: /api/v1/company/<companyID>
    Request methods: GET, PUT, DELETE
    """

    def get(self, companyID):

        company = Company.query.filter_by(companyID=companyID).first()
        if company:
            return marshal(company, company_serializer)
        else:
            return {"error": "A company with ID " + companyID + " does " "not exist."}, 404


    def put(self, companyID):
        company = Company.query.filter_by(companyID=companyID).first()
        if company:
            parser = reqparse.RequestParser()
            parser.add_argument("companyName")
            parser.add_argument("directors")
            parser.add_argument("companyRegistrationNo")
            parser.add_argument("company_phone_number")
            parser.add_argument("companyAddress")
            parser.add_argument("applyCount")
            parser.add_argument("winningCount")
            parser.add_argument("awardedPoint")
            parser.add_argument("isWinner")
            args = parser.parse_args()
            for field in args:
                if args[field] is not None:
                    updated_field = args[field]
                    setattr(company, field, updated_field)
            return create_or_update_resource(resource=company, resource_type="company", serializer=company_serializer, create=False)
        else:
            return {"error": "A company with ID " + companyID + " does not exist."}, 404


    def delete(self, companyID):
        company = Company.query.filter_by(companyID=companyID).first()
        if company:
            return delete_resource(resource=company, resource_type="company", id=companyID)
        else:
            return {"error": "A company with ID " + companyID + " does " "not exist."}, 404
