from src.models import Company
from wtforms import ValidationError
from flask import url_for
from src.company_views import companies
from src.models import Tender, TenderSchema, Company, CompanySchema

# Declear a variable and initalize it to 0 e.g counter = 0
# Check if company registration number does not exist
# if it does exist, return error message for the user ('Company already exist')
# else counter = 1

# init company schema
company_schema = CompanySchema()
companies_schema = CompanySchema(many=True)
# init tender schema
tender_schema = TenderSchema()
tenders_schema = TenderSchema(many=True)


def validate_apply_count(tenderNumber):

    company_list_dict = Company.query.filter_by(tenderNumber=tenderNumber)
    # company_result = companies_schema.dump(comp_list)
    apply_count = 0
    for company_dict in company_list_dict:
        if Company.query.filter_by(tenderNumber=tenderNumber).first():
            # comp_list[]
            apply_count += 1
            raise ValidationError('Company already registered. (Did you mean to ''<a href="{}">log in</a> instead?)'.format(url_for('company.login')))
        else:
            return True


class ValidateCourse:
    """validates the company detail before added to the database

    Returns:
        [boolean] -- [returns true for valid fields and false for invalid fields]
    """

    def __init__(self, data):
        self.data = data

    def validate_apply_count(self):
        """validates the apply_count

        Returns:
            [boolean] -- [True if apply_count is valid else False]
        """
        try:
            if not isinstance(self.data['apply_count'], str) or self.data['apply_count'].isspace() or self.data['apply_count'] == "":
                return False
            else:
                return True
        except KeyError:
            return False

    def validate_winning_count(self):
        """validates the winning_count

        Returns:
            [True] -- [returns true for valid winning_count else false]
        """
        try:
            if self.data['winning_count'] == "" or isinstance(self.data['winning_count'], str):
                return False
            else:
                return True
        except KeyError:
            return False