import jwt
import datetime as dt
from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from src import app, db, login_manager


class User(db.Model, UserMixin):
    """Users will be able to register and login.
    They will also get a token that will allow
    them to make requests.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    @property
    def password(self):
        """Prevents access to password property
        """
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password):
        """Sets password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Checks if password matches
        """
        return check_password_hash(self.password_hash, password)

    def generate_auth_token(self, user_id):
        """Generates the auth token and returns it
        """
        try:
            payload = {
                "exp": dt.datetime.now() + dt.timedelta(
                    days=0, seconds=180000),
                "iat": dt.datetime.now(),
                "sub": user_id
            }
            return jwt.encode(
                payload,
                app.config.get("SECRET_KEY"),
                algorithm="HS256"
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """Decodes the auth token
        """
        try:
            payload = jwt.decode(auth_token, app.config.get("SECRET_KEY"),
                                 options={'verify_iat': False})
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."

    def __repr__(self):
        return "<User: {}>".format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Person(db.Model):

    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email_address = db.Column(db.String(255), unique=True, primary_key=True)
    person_type = db.Column(db.String(50))

    __mapper_args__ = {
        "polymorphic_identity": "person",
        "polymorphic_on": person_type
    }

    def __repr__(self):
        return "<{}: {} {}>".format(self.person_type, self.first_name,
                                    self.last_name)


# Tender Clash/Model
class Tender(db.Model):
    """Tender information
    """
    __tablename__ = "tenders"

    tender_id = db.Column(db.Integer, unique=True, primary_key=True)
    tenderNumber = db.Column(db.String(25), unique=True)
    tenderDescription = db.Column(db.String(80), unique=True)
    category = db.Column(db.String(40), unique=True)
    datePublished = db.Column(db.String(15), unique=True)
    closingDate = db.Column(db.String(15), unique=True)
    tenderStatus = db.Column(db.String(10))
    nameOfInstitution = db.Column(db.String(25), unique=True)
    officalLocation = db.Column(db.String(25), unique=True)
    InstitutionContactPerson = db.Column(db.String(25))
    InstitutionPersonEmail = db.Column(db.String(25))
    InstitutionPersonPhone = db.Column(db.String(15))
    companyName = db.Column(db.String(40), unique=True)
    companyRegistrationNo = db.Column(db.String(30), unique=True)
    directors = db.Column(db.String(50), unique=True)
    cellNumber = db.Column(db.String(15))
    companyAddress = db.Column(db.String(50), unique=True)
    awardedPoint = db.Column(db.String(10))

    def __repr__(self):
        return "<Tender ID: {}>".format(self.tender_id)