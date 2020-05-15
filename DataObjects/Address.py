from sqlalchemy import Table, Column, Integer, String, MetaData
from src.DataAccess.DataAccess import DataAccess
from src.Util.ErrorHandler import InsertError, UpdateError, DeleteError, FetchError


class Address:

    def __init__(self, AddressId, ProvinceId, Line1, Line2, Suburb, City, PostalCode):
        self.meta = MetaData()
        self.data_access = DataAccess()

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsFetched = False

        self.content = Table(
            'Address', self.meta,
            Column('AddressId', Integer, primary_key=True),
            Column('ProvinceId', Integer),
            Column('Line1', String),
            Column('Line2', String),
            Column('Suburb', String),
            Column('City', String),
            Column('PostalCode', String),
        )

        self.AddressId = AddressId
        self.ProvinceId = ProvinceId
        self.Line1 = Line1
        self.Line2 = Line2
        self.Suburb = Suburb
        self.City = City
        self.PostalCode = PostalCode

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

    def DBFetch(self, AddressId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(AddressId)
        except FetchError as fetch_error:
            raise fetch_error

    def _db_insert_check(self):
        pass

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'ProvinceId': self.ProvinceId, 'Line1': self.Line1, 'Line2': self.Line2, 'Suburb': self.Suburb,
                 'City': self.City, 'PostalCode': self.PostalCode},
            ])
            self.AddressId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        pass

    def _db_fetch(self, AddressId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.AddressId == AddressId)
            result = self.data_access.connection.execute(s)

            if result.first() != None:
                raise FetchError('The Address does not exist. Address Id is {0}.'.format(str(AddressId)))
            else:
                # Get results and assign them to class variables
                row = result.first()

                self.AddressId = row[0]
                self.ProvinceId = row[1]
                self.Line1 = row[2]
                self.Line2 = row[3]
                self.Suburb = row[4]
                self.City = row[5]
                self.PostalCode = row[6]
                self.IsFetched = True

    def _db_delete_check(self):
        pass

    def _db_delete(self):
        pass

    def _db_update_check(self):
        pass

    def _db_update(self):
        pass
