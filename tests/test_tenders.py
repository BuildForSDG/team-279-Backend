import json
from app import status
from tests import TestBase

path = "http://127.0.0.1:5000"


class TestTenders(TestBase):
    """Test /tenders endpoint
    """

    def test_list_tenders(self):
        """Test that listing all tenders is successful
        """
        response = self.app.get(path + "/api/v1/tenders", headers=TestBase.get_token(self))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("tenders", response.data.decode('utf-8'))
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual("TENDER105", output["tenders"][0]["tenderNumber"])
        self.assertEqual("Open", output["tenders"][0]["tenderStatus"])

    def test_create_tender(self):
        """Test successful creation of company
        """
        self.tender = {"tenderNumber": "TENDER002",
                       "tenderDescription": "Supply of covid-19 ventilators",
                       "category": "General Health Service",
                       "datePublished": "14/05/2020",
                       "closingDate": "23/06/2020",
                       "tenderStatus": "open",
                       "nameOfInstitution": "Dept of home affairs",
                       "officalLocation": "101 Bellair road",
                       "InstitutionContactPerson": "ola@sample.co.za",
                       "InstitutionPersonEmail": "0117478850",
                       "InstitutionPersonPhone": "boraton2010@gmail.com",
                       "company_names": "{'apply_count': None, 'awardedPoint': 0, 'companyAddress': None, 'companyName': 'Deer', "
                                        "'companyRegistrationNo': None, 'company_id': 4, 'company_phone_number': '277102452112045', "
                                        "'directors': 'ola', 'is_winner': False, 'tenderNumber': 'TENDER002', 'tender_id': 1, "
                                        "'winning_count': None}"
                       }
        response = self.app.post(path + "/api/v1/tenders", data=self.tender, headers=TestBase.get_token(self))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        output = json.loads(response.data.decode('utf-8'))
        self.assertTrue("You have successfully created a new tender" in output["message"])

    def test_missing_field(self):
        """Test that adding a new tender is unsuccessful if
        a required field is missing such as tenderNumber
        """

        self.tender = {"tenderNumber": "",
                       "tenderDescription": "Supply of covid-19 ventilators",
                       "category": "General Health Service",
                       "datePublished": "14/05/2020",
                       "closingDate": "23/06/2020",
                       "tenderStatus": "open",
                       "nameOfInstitution": "Dept of home affairs",
                       "officalLocation": "101 Bellair road",
                       "InstitutionContactPerson": "ola@sample.co.za",
                       "InstitutionPersonEmail": "0117478850",
                       "InstitutionPersonPhone": "boraton2010@gmail.com",
                       "company_names": "{'apply_count': None, 'awardedPoint': 0, 'companyAddress': None, 'companyName': 'Deer', "
                                        "'companyRegistrationNo': None, 'company_id': 4, 'company_phone_number': '277102452112045', "
                                        "'directors': 'ola', 'is_winner': False, 'tenderNumber': 'TENDER105', 'tender_id': 1, "
                                        "'winning_count': None}"
                       }
        response = self.app.post(path + "/api/v1/tenders", data=self.tender, headers=TestBase.get_token(self))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        output = json.loads(response.data.decode('utf-8'))
        expected_response = {"tenderNumber": "Please enter a tender number."}
        self.assertEqual(expected_response, output["message"])


class TestTender(TestBase):
    """Test /tenders/<string:tender_id> endpoint
    """

    def test_get_tender(self):
        """Test that one can see details of selected tender
        """
        response = self.app.get(path + "/api/v1/tenders/TENDER002", headers=TestBase.get_token(self))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual("TENDER002", output["tenderNumber"])
        self.assertEqual("Open", output["tenderStatus"])


    def test_nonexistent_tenderNumber(self):
        """Test that trying to get a tender with a
        non-existent tenderNumber will be unsuccessful
        """
        response = self.app.get(path + "/api/v1/students/TENDER003", headers=TestBase.get_token(self))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual(output, {"error": "A tender with tender number TENDER003 "
                                           "does not exist."})

    def test_update_tender(self):
        """Test that one can update a selected tender.
        Test that only updated fields change while the
        rest remain the same.
        """
        self.tender = {"tenderNumber": "TENDER002"}
        response = self.app.put(path + "/api/v1/tenders/TENDER002", data=self.tender, headers=TestBase.get_token(self))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual("You have successfully edited the tender", output["message"])
        self.assertEqual("Open", output["tenderStatus"])
        self.assertEqual("TENDER002", output["tenderNumber"])

    def test_delete_tender(self):
        """Test that one can delete a selected tender.
        """
        response = self.app.delete(path + "/api/v1/tenders/TENDER002", headers=TestBase.get_token(self))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual(output, {"message": "You have successfully "
                                             "deleted the tender with the following tenderNumber: TENDER002"})
