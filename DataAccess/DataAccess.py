from sqlalchemy import create_engine


class DataAccess:

    def __init__(self):
        self.Username = 'MyDBUser'  # os.environ.get('TUELO_PAY_DB_USERNAME')
        self.Password = 'MyDBUserPassword'  # os.environ.get('TUELO_PAY_DB_PASSWORD')
        self.Host = 'localhost'  # os.environ.get('TUELO_PAY_DB_HOST')
        self.Port = '3306'  # os.environ.get('TUELO_PAY_DB_PORT')
        self.Database = 'MyDBName'  # os.environ.get('TUELO_PAY_DB_DATABASE')

        self.engine = create_engine(
            'mysql+pymysql://' +
            self.Username + ':' + self.Password + '@' + self.Host + ':' + self.Port + '/' + self.Database
        )

        self.connection = self.engine.connect()

    def close_connection(self):
        self.engine.dispose()

    def begin_transaction(self):
        self.connection.begin()

    def commit_transaction(self):
        self.connection.commit()

    def rollback_transaction(self):
        self.connection.rollback()
