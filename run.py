from app import api, app
from app.resources import Index
from app.resources.auth import UserLogin, UserRegister
from app.resources.tenders import TenderListAPI, TenderAPI, CombinedListAPI, CombinedAPI
from app.resources.company import CompanyListAPI, CompanyAPI
# from app.resources.combined_data import CombinedListAPI

""" Defining the API endpoints """
api.add_resource(Index, "")
api.add_resource(UserRegister, "/auth/register")
api.add_resource(UserLogin, "/auth/login")
api.add_resource(TenderListAPI, "/tenders")
api.add_resource(TenderAPI, "/tender/<string:tenderID>")
api.add_resource(CombinedAPI, "/one-tender/<string:tenderNumber>")
api.add_resource(CombinedListAPI, "/combined-tenders")
api.add_resource(CompanyListAPI, "/company")
api.add_resource(CompanyAPI, "/company/<string:companyID>")



if __name__ == "__main__":
    app.run()
