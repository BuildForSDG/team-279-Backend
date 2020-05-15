from sqlalchemy import Table, Column, Integer, String, MetaData
from src.DataAccess.DataAccess import DataAccess
from src.Util.ErrorHandler import InsertError, UpdateError, DeleteError, FetchError


class Country:

    def __init__(self, CountryId, Name):
        self.meta = MetaData()
        self.data_access = DataAccess()

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsFetched = False

        self.content = Table(
            'Country', self.meta,
            Column('CountryId', Integer, primary_key=True),
            Column('Name', String),
        )

        self.CountryId = CountryId
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

    def DBFetch(self, CountryId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(CountryId)
        except FetchError as fetch_error:
            raise fetch_error

    def _db_insert_check(self):
        pass

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'Name': self.Name},
            ])
            self.CountryId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        pass

    def _db_fetch(self, CountryId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.CountryId == CountryId)
            result = self.data_access.connection.execute(s)

            if result.first() != None:
                raise FetchError('The Country does not exist. Country Id is {0}.'.format(str(CountryId)))
            else:
                # Get results and assign them to class variables
                row = result.first()

                self.CountryId = row[0]
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
