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
        SECRET_KEY = os.environ.get('SECRET_KEY')
        SQLALCHEMY_DATABASE_URI = "postgres://ekbokvhsequjic:" \
                                  "3d22c72785ef157cb88bf6839e1091514c" \
                                  "7e5adc551d10fc033cf0f7110392b9@" \
                                  "ec2-52-20-248-222.compute-1" \
                                  ".amazonaws.com:" \
                                  "5432/dv7t90hhoet9i"
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    else:
        DEBUG = False
        TESTING = False
        SECRET_KEY = os.environ.get('SECRET_KEY')
        SQLALCHEMY_DATABASE_URI = \
            os.environ['DATABASE_URL'] \
            or "sqlite:///" + os.path.join(basedir, 'db.sqlite')
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
    SQLALCHEMY_DATABASE_URI = \
        os.getenv("TEST_DATABASE_URI") \
        or "sqlite:///" + os.path.join(basedir, 'testdb.sqlite')
    PRESERVE_CONTEXT_ON_EXCEPTION = False


app_config = {

    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig

}
