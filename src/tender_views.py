from flask import abort, request, jsonify, Blueprint
from src import db, session

tenders = Blueprint('tenders', __name__)

from src.models import Tender, Company, TenderSchema, CompanySchema

# init schema
tender_schema = TenderSchema()
tenders_schema = TenderSchema(many=True)

company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)


@tenders.route('/api/v1/tender/<tender_id>/company/<company_id>', methods=['GET'])
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

    # Was a company found?
    if company is not None:
        data = company_schema.dump(company)
        return jsonify(data)

    # Otherwise, nope, didn't find that note
    else:
        abort(404, "Company not found for Id: {}".format(company_id))


# Get one tender
@tenders.route('/api/v1/tender/<tender_id>', methods=['GET'])
def get_one_tender(tender_id):
    """
    This function responds to a request for /api/vi/tender/<tender_id>
    with one matching tender from companies
    :param tender_id:   Id of tender to find
    :return:            tender matching id
    """
    # Build the initial query
    tender = (Tender.query.filter(Tender.tender_id == tender_id).outerjoin(Company).one_or_none())
    # Did we find a tender?
    if tender is not None:
        # Serialize the data for the response
        data = tender_schema.dump(tender)
        return jsonify(data)
    # Otherwise, nope, didn't find that tender
    else:
        abort(404, "Tender not found for Id: {}".format(tender_id))


# Get All products
@tenders.route('/api/v1/tenders', methods=['GET'])
def get_tenders():
    """
    View all tenders
    URL: /api/v1/tenders
    Request methods: GET
    """
    all_tenders = Tender.query.all()
    result = tenders_schema.dump(all_tenders)
    return jsonify(result)


# Get All tender application products
@tenders.route('/api/v1/all_tenders_object', methods=['GET'])
def get_all():
    """
    View all tenders
    URL: /api/v1/all_tenders_object
    Request methods: GET
    """
    if request.method == 'GET':
        company_query = Company.query.filter()
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
            tender_client = db.session.query(Tender).filter()
            tender_records = tenders_schema.dump(tender_client)
            if tender_client:
                return jsonify(tender_records)
            else:
                return {"error": "A tender does not exist."}, 404
    else:
        return {"error": "Specified tender doesn't exit!"}, 404


# Create a Tender
@tenders.route('/api/v1/tenders', methods=['POST'])
def add_tender():
    if request.method == 'POST':
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
        global_apply_count = request.json['global_apply_count']
        global_winning_count = request.json['global_winning_count']

        new_tender = Tender(tenderNumber, tenderDescription, category, datePublished, closingDate, tenderStatus,
                            nameOfInstitution, officalLocation, InstitutionContactPerson, InstitutionPersonEmail,
                            InstitutionPersonPhone, global_apply_count, global_winning_count)

        db.session.add(new_tender)
        db.session.commit()

        return str(new_tender)
    else:
        return {"error": "Specified tender doesn't exit!"}, 404


# Update Product
@tenders.route('/api/v1/tenders/<tender_id>', methods=['PUT'])
def update_tender(tender_id):
    """
    update a single tender.
    URL: /api/v1/tenders/<tender_id>
    Request methods: PUT
    """
    tender = Tender.query.get(tender_id)
    if tender:
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
        company_names = request.json['company_names']
        global_apply_count = request.json['global_apply_count']
        global_winning_count = request.json['global_winning_count']

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
        tender.company_names = company_names
        tender.global_apply_count = global_apply_count
        tender.global_winning_count = global_winning_count

        db.session.commit()

        return tender_schema.jsonify(tender)
    else:
        return {"error": "A tender with ID " + tender_id + " does not exist."}, 404


# Delete Product
@tenders.route('/api/v1/tenders/<tender_id>', methods=['DELETE'])
def delete_tender(tender_id):
    """
    delete a single tender.
    URL: /api/v1/tenders/<tender_id>
    Request methods: DELETE
    pydocstyle - -ignore = D101, D213
    """
    tender = Tender.query.get(tender_id)
    if tender:
        db.session.delete(tender)
        db.session.commit()
        return tender_schema.jsonify(tender)
    else:
        return {"error": "A tender with ID " + tender_id + " does not exist."}, 404


@tenders.route('/api/v1/tenders/<tenderNumber>/', methods=['GET'])
def get_tender(tenderNumber):
    tender = Tender.query.filter_by(tenderNumber=tenderNumber)

    if tender:
        return tenders_schema.jsonify(tender)
    else:
        return {"error": "A tender with ID " + tenderNumber + " does not exist."}, 404


@tenders.route('/api/v1/displayCompany/<tenderNumber>', methods=['GET'])
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
