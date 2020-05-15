from sqlalchemy import Table, Column, Integer, String, MetaData
from src.DataAccess.DataAccess import DataAccess
from src.Util.ErrorHandler import InsertError, UpdateError, DeleteError, FetchError


class Institution:

    def __init__(self, InstitutionId, Name):
        self.meta = MetaData()
        self.data_access = DataAccess()

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsFetched = False

        self.content = Table(
            'Institution', self.meta,
            Column('InstitutionId', Integer, primary_key=True),
            Column('Name', String),
        )

        self.InstitutionId = InstitutionId
        self.Name = Name

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

    def DBFetch(self, InstitutionId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(InstitutionId)
        except FetchError as fetch_error:
            raise fetch_error

    def _db_insert_check(self):
        pass

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'Name': self.Name},
            ])
            self.InstitutionId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        pass

    def _db_fetch(self, InstitutionId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.InstitutionId == InstitutionId)
            result = self.data_access.connection.execute(s)

            if result.first() != None:
                raise FetchError('The Institution does not exist. Institution Id is {0}.'.format(str(InstitutionId)))
            else:
                # Get results and assign them to class variables
                row = result.first()

                self.InstitutionId = row[0]
                self.Name = row[1]
                self.IsFetched = True

    def _db_delete_check(self):
        pass

    def _db_delete(self):
        pass

    def _db_update_check(self):
        pass

    def _db_update(self):
        pass
