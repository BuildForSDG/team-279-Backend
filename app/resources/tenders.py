from flask import request, jsonify
from flask_restful import Resource, reqparse, marshal
from app import db
from app.resources import create_or_update_resource, delete_resource
from app.models import Tender, TenderSchema, CompanySchema, Company
from app.serializers import tender_serializer

# init schema
tender_schema = TenderSchema()
tenders_schema = TenderSchema(many=True)

company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)


class TenderListAPI(Resource):
    """View all tenders; add new tender
    URL: /api/v1/tenders
    Request methods: POST, GET
    """


    def get(self):

        args = request.args.to_dict()
        page = int(args.get("page", 1))
        limit = int(args.get("limit", 20))
        kwargs = {}

        tenders = Tender.query.filter_by(**kwargs).paginate(page=page, per_page=limit, error_out=False)
        page_count = tenders.pages
        has_next = tenders.has_next
        has_previous = tenders.has_prev
        if has_next:
            next_page = str(request.url_root) + "api/v1.0/tenders?" + \
                "limit=" + str(limit) + "&page=" + str(page + 1)
        else:
            next_page = "None"
        if has_previous:
            previous_page = request.url_root + "api/v1.0/tenders?" + \
                "limit=" + str(limit) + "&page=" + str(page - 1)
        else:
            previous_page = "None"
        tenders = tenders.items

        output = {"tenders": marshal(tenders, tender_serializer),
                  "has_next": has_next,
                  "page_count": page_count,
                  "previous_page": previous_page,
                  "next_page": next_page
                  }

        if tenders:
            return output
        else:
            return {"error": "There are no registered tenders. Add a new one and try again!"}, 404


    def post(self):
        """

        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument("tenderNumber", required=True,help="Please enter a tender number.")
        parser.add_argument("tenderDescription", required=True,help="Please enter a tender description.")
        parser.add_argument("category", required=True, help="Please enter an tender category.")
        parser.add_argument("datePublished", help="Please enter tender date publish date.")
        parser.add_argument("closingDate", help="Please enter tender closing date.")
        parser.add_argument("tenderStatus", help="Please enter a tender status.")
        parser.add_argument("nameOfInstitution", required=True, help="Please enter name of institution.")
        parser.add_argument("officalLocation", required=True, help="Please enter an tender offical location.")
        parser.add_argument("InstitutionContactPerson", help="Please enter tender institution contact person.")
        parser.add_argument("InstitutionPersonEmail", help="Please enter tender institution person email.")
        parser.add_argument("InstitutionPersonPhone", required=True, help="Please enter a tender institution person phone.")

        args = parser.parse_args()
        tenderNumber = args["tenderNumber"]
        tenderDescription = args["tenderDescription"]
        category = args["category"]
        datePublished = args["datePublished"]
        closingDate = args["closingDate"]
        tenderStatus = args["tenderStatus"]
        nameOfInstitution = args["nameOfInstitution"]
        officalLocation = args["officalLocation"]
        InstitutionContactPerson = args["InstitutionContactPerson"]
        InstitutionPersonEmail = args["InstitutionPersonEmail"]
        InstitutionPersonPhone = args["InstitutionPersonPhone"]

        tender = Tender(tenderNumber=tenderNumber,
                        tenderDescription=tenderDescription,
                        category=category,
                        datePublished=datePublished,
                        closingDate=closingDate,
                        tenderStatus=tenderStatus,
                        nameOfInstitution=nameOfInstitution,
                        officalLocation=officalLocation,
                        InstitutionContactPerson=InstitutionContactPerson,
                        InstitutionPersonEmail=InstitutionPersonEmail,
                        InstitutionPersonPhone=InstitutionPersonPhone)
        return create_or_update_resource(resource=tender, resource_type="tender", serializer=tender_serializer, create=True)


class TenderAPI(Resource):
    """View, update and delete a single tender.
    URL: /api/v1/tenders/<tender_id>
    Request methods: GET, PUT, DELETE
    """

    def get(self, tender_id):

        tender = Tender.query.filter_by(tender_id=tender_id).first()
        if tender:
            return marshal(tender, tender_serializer)
        else:
            return {"error": "A tender with tender ID " + tender_id + " does "
                             "not exist."}, 404


    def put(self, tender_id):

        tender = Tender.query.filter_by(tender_id=tender_id).first()
        if tender:
            parser = reqparse.RequestParser()
            parser.add_argument("tenderNumber")
            parser.add_argument("tenderDescription")
            parser.add_argument("category")
            parser.add_argument("datePublished")
            parser.add_argument("closingDate")
            parser.add_argument("tenderStatus")
            parser.add_argument("nameOfInstitution")
            parser.add_argument("officalLocation")
            parser.add_argument("InstitutionContactPerson")
            parser.add_argument("InstitutionPersonEmail")
            parser.add_argument("InstitutionPersonPhone")

            args = parser.parse_args()

            for field in args:
                if args[field] is not None:
                    updated_field = args[field]
                    setattr(tender, field, updated_field)
        else:
            return {"error": "A tender with ID " + tender_id + " does "
                             "not exist."}, 404

        return create_or_update_resource(
            resource=tender,
            resource_type="tender",
            serializer=tender_serializer,
            create=False)


    def delete(self, tender_id):

        tender = Tender.query.filter_by(tender_id=tender_id).first()
        if tender:
            return delete_resource(resource=tender,
                                   resource_type="tender",
                                   id=tender_id)
        else:
            return {"error": "A tender with ID " + tender_id + " does "
                             "not exist."}, 404


class CombinedListAPI(Resource):
    """View all tenders; add new tender
    Request methods: POST, GET
    """

    def get(self):
        """
        View all tenders
        URL: /api/v1/combined-tenders
        Request methods: GET
        """

        # company_query = Company.query.filter_by()
        # company_list_dictionary = companies_schema.dump(company_query)
        # tender_client = db.session.query(Tender).filter_by()
        # tender_list_of_dict = tenders_schema.dump(tender_client)
        # for tender_dict in tender_list_of_dict:
        #     for company_names_dict in company_list_dictionary:
        #         for row in Tender.query.filter_by(tenderNumber=str(tender_dict['tenderNumber'])):
        #             if company_names_dict['tenderNumber'] == row.tenderNumber:
        #                 row.company_names = {"apply_count": company_names_dict['apply_count'],
        #                                      "awardedPoint": company_names_dict['awardedPoint'],
        #                                      "companyAddress": company_names_dict['tender_id'],
        #                                      "companyName": company_names_dict['companyName'],
        #                                      "companyRegistrationNo": company_names_dict['tender_id'],
        #                                      "company_id": company_names_dict['company_id'],
        #                                      "company_phone_number": company_names_dict['company_phone_number'],
        #                                      "directors": company_names_dict['directors'],
        #                                      "is_winner": company_names_dict['is_winner'],
        #                                      "tenderNumber": row.tenderNumber,
        #                                      "tender_id": row.tender_id,
        #                                      "winning_count": company_names_dict['winning_count']
        #                                      }
        #                 db.session.commit()
        tender_client = db.session.query(Tender).all()
        tender_records = tenders_schema.dump(tender_client)
        if tender_records:
            return marshal(tender_records, tender_serializer)
        else:
            return {"error": "A tender with tender ID " + tender_id + " does not exist."}, 404


class CombinedAPI(Resource):
    """View all tenders; add new tender
    Request methods: POST, GET
    """

    def get(self, tenderNumber):
        """
        View all tenders
        URL: /api/v1/one_tender/<string:tenderNumber>
        Request methods: GET
        """

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
        tender_records = tenders_schema.dump(tender_client)

        if tender_records:
            return marshal(tender_records, tender_serializer)
        else:
            return {"error": "A tender with tender ID " + tender_id + " does not exist."}, 404
        #
        # if tender_client:
        #     return jsonify(tender_records)
        # else:
        #     return {"error": "A tender with ID " + tenderNumber + " does not exist."}, 404
    # else:
    #     return {"error": "Specified tender doesn't exit!"}, 404
