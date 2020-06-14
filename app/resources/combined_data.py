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


class CombinedListAPI():
    """View all tenders; add new tender
    Request methods: POST, GET
    """

    def get_combined_all(self):
        """
        View all tenders
        URL: /api/v1/combined-tenders
        Request methods: GET
        """

        company_query = Company.query.filter_by()
        company_list_dictionary = companies_schema.dump(company_query)
        tender_client = db.session.query(Tender).filter_by()
        tender_list_of_dict = tenders_schema.dump(tender_client)
        for tender_dict in tender_list_of_dict:
            for company_names_dict in company_list_dictionary:
                for row in Tender.query.filter_by(tenderNumber=str(tender_dict['tenderNumber'])):
                    if company_names_dict['tenderNumber'] == row.tenderNumber:
                        row.company_names = {"apply_count": company_names_dict['apply_count'],
                                             "awardedPoint": company_names_dict['awardedPoint'],
                                             "companyAddress": company_names_dict['tender_id'],
                                             "companyName": company_names_dict['companyName'],
                                             "companyRegistrationNo": company_names_dict['tender_id'],
                                             "company_id": company_names_dict['company_id'],
                                             "company_phone_number": company_names_dict['company_phone_number'],
                                             "directors": company_names_dict['directors'],
                                             "is_winner": company_names_dict['is_winner'],
                                             "tenderNumber": row.tenderNumber,
                                             "tender_id": row.tender_id,
                                             "winning_count": company_names_dict['winning_count']
                                             }
                        db.session.commit()
            tender_client = db.session.query(Tender).all()
            tender_records = tenders_schema.dump(tender_client)
            if tender_records:
                return marshal(tender_records, tender_serializer)
            else:
                return {"error": "A tender with tender ID " + tender_id + " does not exist."}, 404



            # if tender_client:
            #     return jsonify(tender_records)
            # else:
            #     return {"error": "A tender does not exist."}, 404
    # else:
    #     return {"error": "Specified tender doesn't exit!"}, 404


    def get_individual_tender(self, tenderNumber):
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
