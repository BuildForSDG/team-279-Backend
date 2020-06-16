# User Model
import jwt
import datetime as dt
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.dialects import sqlite
from app import db, app, login_manager, ma
from marshmallow import fields
from sqlalchemy.dialects.postgresql import JSON


class User(db.Model, UserMixin):
    """
    Users will be able to register and login.
    They will also get a token that will allow them to make requests.
    """

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(50), unique=True, index=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)

    @property
    def password(self):
        """Prevents access to password property."""
        raise AttributeError("Password is not a readable attribute.")

    @password.setter
    def password(self, password):
        """Sets password to a hashed password. That is,
        which ensures that the password can never be accessed;
        instead an error will be raised."""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Checks if password matches. That is,
         allow us to ensure the hashed password matches the password
         """
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_auth_token(user_id):
        """Generates the auth token and returns it. That is
        generate_password_hash, allows us to hash passwords
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
        """Decodes the auth token."""
        try:
            payload = jwt.decode(auth_token, app.config.get("SECRET_KEY"),
                                 options={'verify_iat': False})
            return payload["sub"]
        except jwt.ExpiredSignatureError:
            return "Signature expired. Please log in again."
        except jwt.InvalidTokenError:
            return "Invalid token. Please log in again."

    def __repr__(self):
        """
        :param: username.
        :return:
        """
        return "<User: {}>".format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    """Flask-Login uses this to reload the user object from the user ID stored in the session.
    :param user_id:
    :return:
    """
    return User.query.get(int(user_id))


# For the many-to-many relationship between Tenders and companies.
# One company can apply for several Tender and one tender can
# be apply for by several companies
# https://docs.sqlalchemy.org/en/13/orm/basic_relationships.html

# association_table = db.Table("association", db.Model.metadata,
#                              db.Column("tender_id", db.Integer, db.ForeignKey("tenders.tender_id")),
#                              db.Column("company_id", db.Integer, db.ForeignKey("companies.company_id"))
#                              )

# Tender Model


class Tender(db.Model):
    __tablename__ = 'tenders'

    tenderID = db.Column(db.Integer, primary_key=True, nullable=False)
    tenderNumber = db.Column(db.String(25), nullable=False, unique=True)
    tenderDescription = db.Column(db.String(80), nullable=False)
    category = db.Column(db.String(40), nullable=False)
    datePublished = db.Column(db.String(15), nullable=False)
    closingDate = db.Column(db.String(15), nullable=False)
    tenderStatus = db.Column(db.String(10), nullable=False)
    nameOfInstitution = db.Column(db.String(60), nullable=False)
    officalLocation = db.Column(db.String(60), nullable=False)
    InstitutionContactPerson = db.Column(db.String(60), nullable=False)
    InstitutionPersonEmail = db.Column(db.String(60), nullable=False)
    InstitutionPersonPhone = db.Column(db.String(60), nullable=False)
    companyNames = db.Column(sqlite.JSON, server_default='{}')
    company = db.relationship('Company', backref="tenders", cascade='all, delete, delete-orphan', single_parent=True,
                              order_by='desc(Company.companyID)')

    def __init__(self, tenderNumber, tenderDescription, category, datePublished, closingDate, tenderStatus,
                 nameOfInstitution, officalLocation, InstitutionContactPerson, InstitutionPersonEmail,
                 InstitutionPersonPhone):
        """:param tenderNumber:
        :param tenderDescription:
        :param category:
        :param datePublished:
        :param closingDate:
        :param tenderStatus:
        :param nameOfInstitution:
        :param officalLocation:
        :param InstitutionContactPerson:
        :param InstitutionPersonEmail:
        :param InstitutionPersonPhone:
        """

        self.tenderNumber = tenderNumber
        self.tenderDescription = tenderDescription
        self.category = category
        self.datePublished = datePublished
        self.closingDate = closingDate
        self.tenderStatus = tenderStatus
        self.nameOfInstitution = nameOfInstitution
        self.officalLocation = officalLocation
        self.InstitutionContactPerson = InstitutionContactPerson
        self.InstitutionPersonEmail = InstitutionPersonEmail
        self.InstitutionPersonPhone = InstitutionPersonPhone
        # self.companyNames = companyNames

    def __repr__(self):
        """
        :param: tenderID.
        :return:.
        pydocstyle - -ignore = D101, D213
        """
        return '<tenderID {}>'.format(self.tenderID)

    def update(self, tmp_dict):
        for key, value in tmp_dict.items():
            if hasattr(self, key):
                setattr(self, key, value)


class TenderSchema(ma.Schema):
    class Meta:
        model = Tender
        sqla_session = db.session

        fields = ('tenderID', 'tenderNumber', 'tenderDescription', 'category', 'datePublished', 'closingDate',
                  'tenderStatus', 'nameOfInstitution', 'officalLocation', 'InstitutionContactPerson',
                  'InstitutionPersonEmail', 'InstitutionPersonPhone', 'companyNames')

    company = fields.Nested('TenderCompanySchema', default=[], many=True)


class TenderCompanySchema(ma.Schema):
    """
    This class exists to get around a recursion issue
    """

    companyID = fields.Int()
    tenderID = fields.Int()
    companyName = fields.Str()
    companyRegistrationNo = fields.Str()
    directors = fields.Str()
    companyPhoneNumber = fields.Int()
    companyAddress = fields.Str()
    applyCount = fields.Int()
    winningCount = fields.Int()
    awardedPoint = fields.Int()
    tenderNumber = fields.Int()
    isWinner = fields.Str()


# Company Model
class Company(db.Model):
    __tablename__ = "company"

    companyID = db.Column(db.Integer, primary_key=True, nullable=False)
    companyName = db.Column(db.String(60), nullable=False)
    companyRegistrationNo = db.Column(db.String(50), nullable=False)
    directors = db.Column(db.String(60), nullable=False)
    companyPhoneNumber = db.Column(db.String(15), nullable=False)
    companyAddress = db.Column(db.String(50), nullable=False)
    applyCount = db.Column(db.Integer, unique=True)
    winningCount = db.Column(db.Integer)
    isWinner = db.Column(db.Unicode)
    awardedPoint = db.Column(db.Integer)
    tenderNumber = db.Column(db.String(25), nullable=False)
    tenderID = db.Column(db.Integer, db.ForeignKey("tenders.tenderID"))

    def __init__(self, companyName, directors, companyRegistrationNo, companyPhoneNumber,
                 companyAddress, awardedPoint, tenderNumber, isWinner):
        """:param companyName:
        :param directors:
        :param companyRegistrationNo:
        :param companyPhoneNumber:
        :param companyAddress:
        :param awardedPoint:
        :param tenderNumber:
        """

        self.companyName = companyName
        self.companyRegistrationNo = companyRegistrationNo
        self.directors = directors
        self.companyPhoneNumber = companyPhoneNumber
        self.companyAddress = companyAddress
        # self.applyCount = applyCount
        # self.winningCount = winningCount
        self.awardedPoint = awardedPoint
        self.tenderNumber = tenderNumber
        self.isWinner = isWinner

    def __repr__(self):
        """
        :param: companyID.
        :return:.
        pydocstyle - -ignore = D101, D213
        """
        return '<tenderID {}>'.format(self.companyID)



class CompanySchema(ma.Schema):
    class Meta:
        model = Company
        sqla_session = db.session

        fields = ('companyName', 'directors', 'companyRegistrationNo', 'companyPhoneNumber',
                  'companyAddress', 'awardedPoint', 'applyCount', 'winningCount',
                  'tenderID', 'companyID', 'tenderNumber', 'isWinner')

    tender = fields.Nested('CompanyTenderSchema', default=None)


class CompanyTenderSchema(ma.Schema):
    """
    This class exists to get around a recursion issue
    """

    tenderID = fields.Int()
    tenderNumber = fields.Str()
    tenderDescription = fields.Str()
    category = fields.Str()
    datePublished = fields.Str()
    closingDate = fields.Str()
    tenderStatus = fields.Str()
    nameOfInstitution = fields.Str()
    officalLocation = fields.Str()
    InstitutionContactPerson = fields.Str()
    InstitutionPersonEmail = fields.Str()
    InstitutionPersonPhone = fields.Str()
    companyNames = fields.Str()
