import json
from tests import TestBase
from app import status
from app import __version__


def test_version():
    assert __version__ == '0.1.0'


class TestAuth(TestBase):

    def test_index(self):
        """
        Test response to the index route
        """
        response = self.app.get("/api/v1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        output = json.loads(response.data.decode('utf-8'))
        self.assertEqual(output, {"message": "Welcome to the Tender APP API."})

    def test_no_token(self):
        """
        Test that users must provide a token to make requests
        to protected endpoints
        """
        response = self.app.get("/api/v1/tenders")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        output = json.loads(response.data.decode('utf-8'))
        self.assertTrue("Please enter a token" in output["error"])

        response = self.app.get("/api/v1/company")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        output = json.loads(response.data.decode('utf-8'))
        self.assertTrue("Please enter a token" in output["error"])

        response = self.app.get("/api/v1/tenders/all_tenders_object")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        output = json.loads(response.data.decode('utf-8'))
        self.assertTrue("Please enter a token" in output["error"])


        response = self.app.get("/api/v1/display_tender/<tenderNumber>")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        output = json.loads(response.data.decode('utf-8'))
        self.assertTrue("Please enter a token" in output["error"])


    def test_invalid_token(self):
        """
        Test that invalid tokens cannot be used for protected endpoints
        """
        response = self.app.get("/api/v1/tenders", headers={"Authorization": "1234"})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        output = json.loads(response.data.decode('utf-8'))
        self.assertTrue("Invalid token" in output["error"])
