# Tender Clash/Model
from src.app import db


class Tender(db.Model):
    tender_id = db.Column(db.Integer, primary_key=True)
    tenderNumber = db.Column(db.String(25), unique=True)
    tenderDescription = db.Column(db.String(80))
    category = db.Column(db.String(40))
    datePublished = db.Column(db.String(15))
    closingDate = db.Column(db.String(15))
    tenderStatus = db.Column(db.String(10))
    nameOfInstitution = db.Column(db.String(25))
    officalLocation = db.Column(db.String(25))
    InstitutionContactPerson = db.Column(db.String(25))
    InstitutionPersonEmail = db.Column(db.String(25))
    InstitutionPersonPhone = db.Column(db.String(15))
    companyName = db.Column(db.String(40))
    companyRegistrationNo = db.Column(db.String(30))
    directors = db.Column(db.String(50))
    cellNumber = db.Column(db.String(15))
    companyAddress = db.Column(db.String(50))
    awardedPoint = db.Column(db.String(10))

    def __init__(self, tenderNumber, tenderDescription, category, datePublished, closingDate, tenderStatus,
                 nameOfInstitution, officalLocation, InstitutionContactPerson, InstitutionPersonEmail,
                 InstitutionPersonPhone, companyName, companyRegistrationNo, directors, cellNumber, companyAddress,
                 awardedPoint):
        """

        :param tenderNumber:
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
        :param companyName:
        :param companyRegistrationNo:
        :param directors:
        :param cellNumber:
        :param companyAddress:
        :param awardedPoint:
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
        self.companyName = companyName
        self.companyRegistrationNo = companyRegistrationNo
        self.directors = directors
        self.cellNumber = cellNumber
        self.companyAddress = companyAddress
        self.awardedPoint = awardedPoint

    def __repr__(self):

        """
        :param: tender_id.
        :return:
        """

        return '<tender_id {}>'.format(self.tender_id)
