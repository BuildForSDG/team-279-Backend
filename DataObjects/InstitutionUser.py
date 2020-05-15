from sqlalchemy import Table, Column, Integer, String, MetaData
from src.DataAccess.DataAccess import DataAccess
from src.Util.ErrorHandler import InsertError, UpdateError, DeleteError, FetchError


class InstitutionUser:

    def __init__(self, InstitutionUserId, InstitutionId, Firstname, Middlename, Lastname, EmailAddress, Password):
        self.meta = MetaData()
        self.data_access = DataAccess()

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsFetched = False

        self.content = Table(
            'InstitutionUser', self.meta,
            Column('InstitutionUserId', Integer, primary_key=True),
            Column('InstitutionId', Integer),
            Column('Firstname', String),
            Column('Middlename', String),
            Column('Lastname', String),
            Column('EmailAddress', String),
            Column('Password', String),
        )

        self.InstitutionUserId = InstitutionUserId
        self.InstitutionId = InstitutionId
        self.Firstname = Firstname
        self.Middlename = Middlename
        self.Lastname = Lastname
        self.EmailAddress = EmailAddress
        self.Password = Password

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

    def DBFetch(self, InstitutionUserId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(InstitutionUserId)
        except FetchError as fetch_error:
            raise fetch_error

    def _db_insert_check(self):
        pass

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'InstitutionId': self.InstitutionId, 'Firstname': self.Firstname, 'Middlename': self.Middlename,
                 'Lastname': self.Lastname, 'EmailAddress': self.EmailAddress, 'Password': self.Password},
            ])
            self.InstitutionUserId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        pass

    def _db_fetch(self, InstitutionUserId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.InstitutionUserId == InstitutionUserId)
            result = self.data_access.connection.execute(s)

            if result.first() != None:
                raise FetchError(
                    'The InstitutionUser does not exist. InstitutionUser Id is {0}.'.format(str(InstitutionUserId)))
            else:
                # Get results and assign them to class variables
                row = result.first()

                self.InstitutionUserId = row[0]
                self.InstitutionId = row[1]
                self.Firstname = row[2]
                self.Middlename = row[3]
                self.Lastname = row[4]
                self.EmailAddress = row[5]
                self.Password = row[6]
                self.IsFetched = True

    def _db_delete_check(self):
        pass

    def _db_delete(self):
        pass

    def _db_update_check(self):
        pass

    def _db_update(self):
        pass
