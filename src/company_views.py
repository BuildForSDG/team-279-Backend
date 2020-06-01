from flask import abort, request, jsonify, Blueprint
from src import db
from src.models import Tender, TenderSchema, Company, CompanySchema

companies = Blueprint('companies', __name__)

# init company schema
company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)
# init tender schema
tender_schema = TenderSchema()
tenders_schema = TenderSchema(many=True)


@companies.route('/api/v1/display_company/<tenderNumber>', methods=['GET'])
def display_company(tenderNumber):
    if request.method == 'GET':
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
        tenders = tenders_schema.dump(tender_client)
        if tender_client:
            return jsonify(tenders)
        else:
            return {"error": "A tender with ID " + tenderNumber + " does not exist."}, 404
    else:
        return {"error": "Specified tender doesn't exit!"}, 404


# Get All companies
@companies.route('/api/v1/companies', methods=['GET'])
def get_all_companies():
    """
    View all companies
    URL: /api/v1/companies
    Request methods: GET
    """
    all_companies = Company.query.all()
    company_result = companies_schema.dump(all_companies)
    return jsonify(company_result)


# Get one company
@companies.route('/api/v1/company/<company_id>', methods=['GET'])
def get_one_company(company_id):
    """
    This function responds to a request for /api/vi/company/<company_id>
    with one matching company from companies
    :param company_id:   Id of company to find
    :return:            company matching id
    """
    # Build the initial query
    company = (Company.query.filter(Company.company_id == company_id).outerjoin(Tender).one_or_none())
    # Did we find a company?
    if company is not None:
        # Serialize the data for the response
        data = company_schema.dump(company)
        return jsonify(data)
    # Otherwise, nope, didn't find that company
    else:
        abort(404, "Company not found for Id: {}".format(company_id))


@companies.route('/api/v1/post_company/<tenderNumber>', methods=['POST'])
def post_company(tenderNumber):
    if request.method == 'POST':
        companyName = request.json['companyName']
        directors = request.json['directors']
        companyRegistrationNo = request.json['companyRegistrationNo']
        company_phone_number = request.json['company_phone_number']
        companyAddress = request.json['companyAddress']
        awardedPoint = request.json['awardedPoint']
        new_company = Company(companyName, directors, companyRegistrationNo, company_phone_number,
                              companyAddress, awardedPoint, tenderNumber)
        db.session.add(new_company)
        db.session.commit()
        return str(new_company)
    else:
        return {"error": "Specified tender doesn't exit!"}, 404


@companies.route('/api/v1/tender/<tender_id>/company/<company_id>', methods=['GET'])
def read_one(tender_id, company_id):
    """
    This function responds to a request for
    /api/v1/tender/{tender_id}/companies/{company_id}
    with one matching company for the associated tender

    :param tender_id:       Id of tender the company is related to
    :param company_id:         Id of the company
    :return:                json string of company contents
    """
    # Query the database for the company
    company = (
        Company.query.join(Tender, Tender.tender_id == Company.tender_id).filter(Tender.tender_id == tender_id).filter(
            Company.company_id == company_id).all())

    # company = (Tender.query.join(Company, Company.tender_id == Tender.tender_id).filter(Company.tender_id == tender_id).filter(Tender.company_id == company_id).one_or_none())
    # company = db.session.query(Company, Tender).filter(Company.company_id == Tender.tender_id).all()
    # Was a company found?
    if company is not None:
        data = company_schema.dump(company)
        return jsonify(data)

    # Otherwise, nope, didn't find that note
    else:
        abort(404, "Company not found for Id: {}".format(company_id))


@companies.route('/api/v1/edit-company/<tenderNumber>', methods=['PUT'])
def edit_company(tenderNumber):
    company = Company.query.filter_by(tenderNumber=tenderNumber).first()
    if request.method == 'PUT':
        companyName = request.json['companyName']
        directors = request.json['directors']
        companyRegistrationNo = request.json['companyRegistrationNo']
        company_phone_number = request.json['company_phone_number']
        companyAddress = request.json['companyAddress']
        apply_count = request.json['apply_count']
        winning_count = request.json['winning_count']
        awardedPoint = request.json['awardedPoint']

        company.companyName = companyName
        company.companyRegistrationNo = companyRegistrationNo
        company.directors = directors
        company.company_phone_number = company_phone_number
        company.companyAddress = companyAddress
        company.apply_count = apply_count
        company.winning_count = winning_count
        company.awardedPoint = awardedPoint

        db.session.commit()

        return company_schema.jsonify(company)
    else:
        return {"error": "A company with tenderNumber " + tenderNumber + " does not exist."}, 404


@companies.route('/api/v1/delete-company/<tenderNumber>/<company_id>', methods=['DELETE'])
def delete_company(tenderNumber, company_id):
    # company = Company.query.filter_by(tenderNumber=tenderNumber).first()
    company = (Company.query.join(Tender, Tender.tenderNumber == Company.tenderNumber).filter(
        Company.company_id == company_id).all())
    if request.method == 'DELETE':
        db.session.delete(company)
        db.session.commit()
        return company_schema.jsonify(company)
    else:
        return {"error": "A company with tenderNumber " + tenderNumber + " does not exist."}, 404
