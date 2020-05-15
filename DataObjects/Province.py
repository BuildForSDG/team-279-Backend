from sqlalchemy import Table, Column, Integer, String, MetaData

from src.DataAccess.DataAccess import DataAccess
from src.Util.ErrorHandler import InsertError, UpdateError, DeleteError, FetchError


class Province:

    def __init__(self, ProvinceId, CountryId, Name):
        self.meta = MetaData()
        self.data_access = DataAccess()

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsFetched = False

        self.content = Table(
            'Province', self.meta,
            Column('ProvinceId', Integer, primary_key=True),
            Column('CountryId', Integer),
            Column('Name', String),
        )

        self.ProvinceId = ProvinceId
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

    def DBFetch(self, ProvinceId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(ProvinceId)
        except FetchError as fetch_error:
            raise fetch_error

    def _db_insert_check(self):
        pass

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'CountryId': self.CountryId, 'Name': self.Name},
            ])
            self.ProvinceId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        pass

    def _db_fetch(self, ProvinceId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.ProvinceId == ProvinceId)
            result = self.data_access.connection.execute(s)

            if result.first() != None:
                raise FetchError('The Province does not exist. Province Id is {0}.'.format(str(ProvinceId)))
            else:
                # Get results and assign them to class variables
                row = result.first()

                self.ProvinceId = row[0]
                self.CountryId = row[1]
                self.Name = row[2]
                self.IsFetched = True

    def _db_delete_check(self):
        pass

    def _db_delete(self):
        pass

    def _db_update_check(self):
        pass

    def _db_update(self):
        pass
