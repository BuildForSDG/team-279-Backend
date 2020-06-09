import json
from app import status
from tests import TestBase

path = "http://127.0.0.1:5000"

class TestCompanies(TestBase):
    """Test /company endpoint
    """

    def test_list_company(self):
        """Test that listing all company is successful
        """
        response = self.app.get(path + "/api/v1/company", headers=TestBase.get_token(self))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("company", response.data.decode('utf-8'))
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual("FNDH/212654911", output["company"][0]["companyRegistrationNo"])
        self.assertEqual("TENDER104", output["company"][0]["tenderNumber"])

    def test_create_company(self):
        """Test successful creation of company
        """
        self.company = {"companyName": "Shell Garage",
                        "companyRegistrationNo": "FNDH/212654911",
                        "directors": "ola",
                        "company_phone_number": "AGL/10245/2112045",
                        "companyAddress": "Cape town",
                        "apply_count": 1,
                        "winning_count": 3,
                        "awardedPoint": 35,
                        "tenderNumber": "TENDER125"
                        }
        response = self.app.post(path + "/api/v1/company", data=self.company, headers=TestBase.get_token(self))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        output = json.loads(response.data.decode('utf-8'))
        self.assertTrue("You have successfully created a new company" in output["message"])

    def test_missing_field(self):
        """Test that adding a new company is unsuccessful if
        a required field is missing
        """

        self.company = {"companyName": "Shell Garage",
                        "companyRegistrationNo": "",
                        "directors": "ola",
                        "company_phone_number": "AGL/10245/2112045",
                        "companyAddress": "Cape town",
                        "apply_count": 1,
                        "winning_count": 3,
                        "awardedPoint": 35,
                        "tenderNumber": ""
                        }
        response = self.app.post(path + "/api/v1/company", data=self.company, headers=TestBase.get_token(self))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        output = json.loads(response.data.decode('utf-8'))
        expected_response = {"companyRegistrationNo": "Please enter valid company registration number."}
        self.assertEqual(expected_response, output["message"])


class TestCompany(TestBase):
    """
    Test /company/<string:company_id> endpoint
    """

    def test_get_company(self):
        """
        Test that one can see details of selected company
        """
        response = self.app.get(path + "/api/v1/company/TENDER125", headers=TestBase.get_token(self))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual("Minerva", output["companyName"])
        self.assertEqual("AGL/10245/2112045", output["companyRegistrationNo"])

    def test_nonexistent_id(self):
        """
        Test that trying to get a company with a
        non-existent ID will be unsuccessful
        """
        response = self.app.get(path + "/api/v1/company/TENDER128", headers=TestBase.get_token(self))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual(output, {"error": "A company with tender number TENDER128 "
                                           "does not exist."})

    def test_update_company(self):
        """Test that one can update a selected company.
        Test that only updated fields change while the
        rest remain the same.
        """
        self.company = {"companyRegistrationNo": "AGL/10245/211",
                        "companyName": "Chevron Oil and Gas"}
        response = self.app.put(path + "/api/v1/company/TENDER128", data=self.company, headers=TestBase.get_token(self))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual("You have successfully edited the company", output["message"])
        self.assertEqual("Chevron Oil and Gas", output["companyName"])
        self.assertEqual("AGL/10245/211", output["companyRegistrationNo"])

    def test_delete_company(self):
        """Test that one can delete a selected company.
        """
        response = self.app.delete(path + "/api/v1/company/TENDER105", headers=TestBase.get_token(self))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual(output, {"message": "You have successfully "
                                             "deleted the company with the following tender number: TENDER105"})
