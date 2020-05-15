from sqlalchemy import Table, Column, Integer, String, MetaData
from src.DataAccess.DataAccess import DataAccess
from src.Util.ErrorHandler import InsertError, UpdateError, DeleteError, FetchError


class CompanyDirector:

    def __init__(self, CompanyDirectorId, CompanyId, Firstname, Middlename, Lastname, IDNumber, PassportNumber):
        self.meta = MetaData()
        self.data_access = DataAccess()

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsFetched = False

        self.content = Table(
            'CompanyDirector', self.meta,
            Column('CompanyDirectorId', Integer, primary_key=True),
            Column('CompanyId', Integer),
            Column('Firstname', String),
            Column('Middlename', String),
            Column('Lastname', String),
            Column('IDNumber', String),
            Column('PassportNumber', String),
        )

        self.CompanyDirectorId = CompanyDirectorId
        self.CompanyId = CompanyId
        self.Firstname = Firstname
        self.Middlename = Middlename
        self.Lastname = Lastname
        self.IDNumber = IDNumber
        self.PassportNumber = PassportNumber

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

    def DBFetch(self, CompanyDirectorId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(CompanyDirectorId)
        except FetchError as fetch_error:
            raise fetch_error

    def _db_insert_check(self):
        pass

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'CompanyId': self.CompanyId, 'Firstname': self.Firstname, 'Middlename': self.Middlename,
                 'Lastname': self.Lastname, 'IDNumber': self.IDNumber, 'PassportNumber': self.PassportNumber},
            ])
            self.CompanyDirectorId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        pass

    def _db_fetch(self, CompanyDirectorId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.CompanyDirectorId == CompanyDirectorId)
            result = self.data_access.connection.execute(s)

            if result.first() != None:
                raise FetchError(
                    'The CompanyDirector does not exist. CompanyDirector Id is {0}.'.format(str(CompanyDirectorId)))
            else:
                # Get results and assign them to class variables
                row = result.first()

                self.CompanyDirectorId = row[0]
                self.CompanyId = row[1]
                self.Firstname = row[2]
                self.Middlename = row[3]
                self.Lastname = row[4]
                self.IDNumber = row[5]
                self.PassportNumber = row[6]
                self.IsFetched = True

    def _db_delete_check(self):
        pass

    def _db_delete(self):
        pass

    def _db_update_check(self):
        pass

    def _db_update(self):
        pass
