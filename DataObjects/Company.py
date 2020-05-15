from sqlalchemy import Table, Column, Integer, String, MetaData
from src.DataAccess.DataAccess import DataAccess
from src.Util.ErrorHandler import InsertError, UpdateError, DeleteError, FetchError


class Company:

    def __init__(self, CompanyId, Name, Registration, RegistrationDate, Status):
        self.meta = MetaData()
        self.data_access = DataAccess()

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsFetched = False

        self.content = Table(
            'Company', self.meta,
            Column('CompanyId', Integer, primary_key=True),
            Column('Name', String),
            Column('Registration', String),
            Column('RegistrationDate', DateTime),
            Column('Status', String),
        )

        self.CompanyId = CompanyId
        self.Name = Name
        self.Registration = Registration
        self.RegistrationDate = RegistrationDate
        self.Status = Status

    def Save(self):
        try:
            if not self.IsInserted:
                self._db_insert_check()
                self._db_insert()
            else:
                self._db_update_check()
                self._db_update()
        except InsertError as insert_error:
            raise insert_error

    def DBFetch(self, CompanyId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(CompanyId)
        except FetchError as fetch_error:
            raise fetch_error

    def _db_insert_check(self):
        pass

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'Name': self.Name, 'Registration': self.Registration, 'RegistrationDate': self.RegistrationDate,
                 'Status': self.Status},
            ])
            self.CompanyId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        pass

    def _db_fetch(self, CompanyId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.CompanyId == CompanyId)
            result = self.data_access.connection.execute(s)

            if result.first() != None:
                raise FetchError('The Company does not exist. Company Id is {0}.'.format(str(CompanyId)))
            else:
                # Get results and assign them to class variables
                row = result.first()

                self.CompanyId = row[0]
                self.Name = row[1]
                self.Registration = row[2]
                self.RegistrationDate = row[3]
                self.Status = row[4]
                self.IsFetched = True

    def _db_delete_check(self):
        pass

    def _db_delete(self):
        pass

    def _db_update_check(self):
        pass

    def _db_update(self):
        pass
