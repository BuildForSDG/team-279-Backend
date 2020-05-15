import os

from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy
from src import app
from . import *
from src.config import app_config





# init ap

def create_app(configuration):
    app = Flask(__name__)
    app.config.from_object(app_config[configuration])
    return app

app = create_app(os.getenv('ENVIRONMENT'))
# init ma
ma = Marshmallow(app)

# init db
db = SQLAlchemy(app)