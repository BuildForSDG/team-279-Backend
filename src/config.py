from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env')
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Common configurations.
    pydocstyle - -ignore = D101, D213
    """
    if os.getenv("ENVIRONMENT") == "production":
        DEBUG = False
        TESTING = False
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
        SQLALCHEMY_DATABASE_URI = 'postgres://gxbsxwxjlbmpot:6e1252a7f2363c49451d93620fd3fe65366a1e785a41d12cbf8d975e37d56780@ec2-34-232-147-86.compute-1.amazonaws.com:5432/d6i9nenaoci57r'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    else:
        DEBUG = False
        TESTING = False
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] or 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
        SQLALCHEMY_TRACK_MODIFICATIONS = False    


class DevelopmentConfig(Config):
    """Development configurations.
    pydocstyle - -ignore = D101, D213
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production configurations.
    pydocstyle - -ignore = D101, D213
    """

    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configurations.
    pydocstyle - -ignore = D101, D213
    """

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URI")
    PRESERVE_CONTEXT_ON_EXCEPTION = False


app_config = {

    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig

}
