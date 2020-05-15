from sqlalchemy import Table, Column, Integer, String, MetaData
from src.DataAccess.DataAccess import DataAccess
from src.Util.ErrorHandler import InsertError, UpdateError, DeleteError, FetchError


class CompanyAddress:

    def __init__(self, CompanyAddressId, CompanyId, AddressId):
        self.meta = MetaData()
        self.data_access = DataAccess()

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsFetched = False

        self.content = Table(
            'CompanyAddress', self.meta,
            Column('CompanyAddressId', Integer, primary_key=True),
            Column('CompanyId', Integer),
            Column('AddressId', Integer),
        )

        self.CompanyAddressId = CompanyAddressId
        self.CompanyId = CompanyId
        self.AddressId = AddressId

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

    def DBFetch(self, CompanyAddressId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(CompanyAddressId)
        except FetchError as fetch_error:
            raise fetch_error

    def _db_insert_check(self):
        pass

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'CompanyId': self.CompanyId, 'AddressId': self.AddressId},
            ])
            self.CompanyAddressId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        pass

    def _db_fetch(self, CompanyAddressId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.CompanyAddressId == CompanyAddressId)
            result = self.data_access.connection.execute(s)

            if result.first() != None:
                raise FetchError(
                    'The CompanyAddress does not exist. CompanyAddress Id is {0}.'.format(str(CompanyAddressId)))
            else:
                # Get results and assign them to class variables
                row = result.first()

                self.CompanyAddressId = row[0]
                self.CompanyId = row[1]
                self.AddressId = row[2]
                self.IsFetched = True

    def _db_delete_check(self):
        pass

    def _db_delete(self):
        pass

    def _db_update_check(self):
        pass

    def _db_update(self):
        pass
