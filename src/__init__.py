""" Application version number. """
__version__ = '0.1.0'

from flask_marshmallow import Marshmallow
from src.config import app_config
from flask_bootstrap import Bootstrap
from flask_cors import CORS
from flask_migrate import Migrate
import os
from flask import Flask
from flask_login import LoginManager
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
login_manager = LoginManager()


# app = Flask(__name__, instance_relative_config=True)
# app.config.from_object(app_config[os.getenv('ENVIRONMENT')])
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db.init_app(app)
# # after the db variable initialization
# login_manager = LoginManager()
# Bootstrap(app)
# login_manager.init_app(app)
# login_manager.login_message = "You must be logged in to access this page."
# login_manager.login_view = "auth.login"


def create_app(config_env):

    if os.getenv('FLASK_CONFIG') == "development":
        app = Flask(__name__)
        app.config.update(SECRET_KEY=os.getenv('SECRET_KEY'), SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY_DATABASE_URI'))
    else:
        app = Flask(__name__, instance_relative_config=True)
        app.config.from_object(app_config[config_env])
        # app.config.from_pyfile('/config.py')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    Bootstrap(app)
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_message = "You must be logged in to access this page."
    login_manager.login_view = "auth.login"
    migrate = Migrate(app, db)

    return app


config_name = os.getenv('ENVIRONMENT')

app = create_app(config_name)
api = Api(app=app, prefix="/api/v1")
# init ma
ma = Marshmallow(app)

from src import models
# from src import tender_views, company_views
# from src.models import Tender, Company, TenderSchema, CompanySchema

# imported each blueprint object and registered it
from src.tender_views import tenders
app.register_blueprint(tenders)
from src.company_views import companies
app.register_blueprint(companies)
