from sqlalchemy import Table, Column, Integer, String, MetaData
from src.DataAccess.DataAccess import DataAccess
from src.Util.ErrorHandler import InsertError, UpdateError, DeleteError, FetchError


class TenderCompany:

    def __init__(self, TenderCompanyId, TenderId, CompanyId, Status):
        self.meta = MetaData()
        self.data_access = DataAccess()

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsFetched = False

        self.content = Table(
            'TenderCompany', self.meta,
            Column('TenderCompanyId', Integer, primary_key=True),
            Column('TenderId', Integer),
            Column('CompanyId', Integer),
            Column('Status', String),
        )

        self.TenderCompanyId = TenderCompanyId
        self.TenderId = TenderId
        self.CompanyId = CompanyId
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

    def DBFetch(self, TenderCompanyId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(TenderCompanyId)
        except FetchError as fetch_error:
            raise fetch_error

    def _db_insert_check(self):
        pass

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'TenderId': self.TenderId, 'CompanyId': self.CompanyId, 'Status': self.Status},
            ])
            self.TenderCompanyId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        pass

    def _db_fetch(self, TenderCompanyId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.TenderCompanyId == TenderCompanyId)
            result = self.data_access.connection.execute(s)

            if result.first() != None:
                raise FetchError(
                    'The TenderCompany does not exist. TenderCompany Id is {0}.'.format(str(TenderCompanyId)))
            else:
                # Get results and assign them to class variables
                row = result.first()

                self.TenderCompanyId = row[0]
                self.TenderId = row[1]
                self.CompanyId = row[2]
                self.Status = row[3]
                self.IsFetched = True

    def _db_delete_check(self):
        pass

    def _db_delete(self):
        pass

    def _db_update_check(self):
        pass

    def _db_update(self):
        pass
