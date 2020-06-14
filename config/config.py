from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env')
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Common configurations.
    pydocstyle - -ignore = D101, D213
    """

    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    if os.getenv("ENVIRONMENT") == "development":
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] or 'sqlite:///' + os.path.join(basedir, 'vtender.sqlite')
    else:
        SQLALCHEMY_DATABASE_URI = 'postgresql:///vtender'
        # SQLALCHEMY_DATABASE_URI = "postgres://lkryctgiwiqcum:180df7d87c07048e60d733f2803f6dca755b929e132289c2ba07a1c8df19fbdf@ec2-34-193-117-204.compute-1.amazonaws.com:5432/d2khvjku62o1bc"

    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development configurations.
    pydocstyle - -ignore = D101, D213
    """

    DEBUG = True
    SQLALCHEMY_ECHO = True


class StagingConfig(Config):
    """

    """
    DEVELOPMENT = True
    DEBUG = True


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
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URI") or 'sqlite:///' + os.path.join(basedir, 'testdb.sqlite')
    PRESERVE_CONTEXT_ON_EXCEPTION = False


app_config = {

    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig

}
