from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='.env')
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    """Common configurations."""

    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'] or 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    """Development configurations."""

    DEBUG = True
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production configurations."""

    DEBUG = False
    TESTING = False


class TestingConfig(Config):
    """Testing configurations."""

    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URI")
    PRESERVE_CONTEXT_ON_EXCEPTION = False


app_config = {

    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig

}
