from sqlalchemy import Table, Column, Integer, String, MetaData
from src.DataAccess.DataAccess import DataAccess
from src.Util.ErrorHandler import InsertError, UpdateError, DeleteError, FetchError


class Tender:

    def __init__(self, TenderId, InstitutionId, Number, Description, Category, PublishedDate, ClosingDate, AwardedDate):
        self.meta = MetaData()
        self.data_access = DataAccess()

        self.IsFetched = False
        self.IsInserted = False
        self.IsUpdated = False
        self.IsFetched = False

        self.content = Table(
            'Tender', self.meta,
            Column('TenderId', Integer, primary_key=True),
            Column('InstitutionId', Integer),
            Column('Number', String),
            Column('Description', String),
            Column('Category', String),
            Column('PublishedDate', DateTime),
            Column('ClosingDate', DateTime),
            Column('AwardedDate', DateTime),
        )

        self.TenderId = TenderId
        self.InstitutionId = InstitutionId
        self.Number = Number
        self.Description = Description
        self.Category = Category
        self.PublishedDate = PublishedDate
        self.ClosingDate = ClosingDate
        self.AwardedDate = AwardedDate

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

    def DBFetch(self, TenderId):
        try:
            if not self.IsInserted and not self.IsFetched:
                self._db_fetch_check()
                self._db_fetch(TenderId)
        except FetchError as fetch_error:
            raise fetch_error

    def _db_insert_check(self):
        pass

    def _db_insert(self):
        if not self.IsInserted and not self.IsFetched and not self.IsUpdated:
            result = self.data_access.connection.execute(self.content.insert(), [
                {'InstitutionId': self.InstitutionId, 'Number': self.Number, 'Description': self.Description,
                 'Category': self.Category, 'PublishedDate': self.PublishedDate, 'ClosingDate': self.ClosingDate,
                 'AwardedDate': self.AwardedDate},
            ])
            self.TenderId = result.inserted_primary_key
            self.IsInserted = True
            self.IsFetched = True

    def _db_fetch_check(self):
        pass

    def _db_fetch(self, TenderId):
        if not self.IsFetched:
            s = self.content.select().where(self.content.c.TenderId == TenderId)
            result = self.data_access.connection.execute(s)

            if result.first() != None:
                raise FetchError('The Tender does not exist. Tender Id is {0}.'.format(str(TenderId)))
            else:
                # Get results and assign them to class variables
                row = result.first()

                self.TenderId = row[0]
                self.InstitutionId = row[1]
                self.Number = row[2]
                self.Description = row[3]
                self.Category = row[4]
                self.PublishedDate = row[5]
                self.ClosingDate = row[6]
                self.AwardedDate = row[7]
                self.IsFetched = True

    def _db_delete_check(self):
        pass

    def _db_delete(self):
        pass

    def _db_update_check(self):
        pass

    def _db_update(self):
        pass
