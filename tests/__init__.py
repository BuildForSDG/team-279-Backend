import json
import os
import unittest
from app import create_app
from app import db
from app.models import Tender, User, Company
from config.config import app_config
from run import app
from unittest import TestCase


path = "http://127.0.0.1:5000"

app.config.from_object(app_config["testing"])


class TestBase(TestCase):
    """Base configurations for the tests
    """

    def create_app(self):
        """Create Flask app
        """

        # app = create_app(os.getenv('ENVIRONMENT'))
        return app

    def get_token(self):
        """Returns authentication token
        """
        self.user = {"username": "testuser",
                     "password": "testpassword"}
        response = self.app.post(path + "/api/v1/auth/login", data=self.user)
        output = json.loads(response.data.decode('utf-8'))
        token = output["token"]
        return {"Authorization": token}



    def setUp(self):
        """Set up test client and populate test database with test data
        """
        # app = create_app()
        with app.app_context():
            self.app = app.test_client()
            self.app_context = app.app_context()
            db.create_all()
            # db.init_app(app)

            user = User(username="testuser", password="testpassword")
            tender = Tender(tenderNumber="TENDER124",
            tenderDescription="Supply of covid-19 ventilators",
            category="General Health Service",
            datePublished="14/05/2020",
            closingDate="23/06/2020",
            tenderStatus="open",
            nameOfInstitution="Dep of home affairs",
            officalLocation="101 Bellair road",
            InstitutionContactPerson="",
            InstitutionPersonEmail="ola@sample.co.za",
            InstitutionPersonPhone="0117478850")

            company = Company(tenderNumber="TENDER124",
                companyName="Deer",
                directors="ola",
                companyRegistrationNo="FNDH/212654911",
                company_phone_number="277102452112045",
                companyAddress="Cape town",
                awardedPoint=0)

            # tender.company_name.append(company)

            db.session.add(user)
            db.session.add(tender)
            db.session.add(company)


    def tearDown(self):
        """Destroy test database
        """
        db.session.remove()
        # self.app_context.pop()
        db.drop_all()



if __name__ == "__main__":
    unittest.main()
