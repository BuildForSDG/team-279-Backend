#!/usr/bin/env python
import os
import subprocess
import flask_migrate
from redis import Redis
from rq import Connection, Queue, Worker
from src.config import Config
from flask_script import Manager, Shell
from src import app, db
from src.models import Tender, Company, User


basedir = os.path.abspath(os.path.dirname(__file__))
migrate = flask_migrate.Migrate(app, db)
manager = Manager(app)
manager.add_command("db", flask_migrate.MigrateCommand)



def make_shell_context():
    """
    :param:.
    :return: application and database instances to the shell importing them automatically on python manager.py shell.
    pydocstyle - -ignore = D101, D213
    """
    return dict(app=app, db=db, Tender=Tender, Company=Company)


manager.add_command("shell", Shell(make_context=make_shell_context))


@manager.command
def test():
    """Run the unit tests."""
    import unittest

    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


@manager.command
def recreate_db():
    """
    Recreates a local database. You probably should not use this on
    production.
    """
    db.drop_all()
    db.create_all()
    db.session.commit()


def setup_prod():
    """Runs the set-up needed for production."""
    setup_general()


def setup_general():
    """Runs the set-up needed for both local development and production.
       Also sets up first admin2 user."""
    User.insert_roles()
    admin_query = User.query.filter_by(name='Administrator')
    if admin_query.first() is not None:
        if User.query.filter_by(email=Config.ADMIN_EMAIL).first() is None:
            user = User(
                first_name='Admin',
                last_name='Account',
                password=Config.ADMIN_PASSWORD,
                confirmed=True,
                email=Config.ADMIN_EMAIL)
            db.session.add(user)
            db.session.commit()
            print('Added administrator {}'.format(user.full_name()))


@manager.command
def run_worker():
    """Initializes a slim rq task queue."""
    listen = ['default']
    conn = Redis(
        host=app.config['RQ_DEFAULT_HOST'],
        port=app.config['RQ_DEFAULT_PORT'],
        db=0,
        password=app.config['RQ_DEFAULT_PASSWORD'])

    with Connection(conn):
        worker = Worker(map(Queue, listen))
        worker.work()


@manager.command
def format():
    """Runs the yapf and isort formatters over the project."""
    isort = 'isort -rc *.py app/'
    yapf = 'yapf -r -i *.py app/'

    print('Running {}'.format(isort))
    subprocess.call(isort, shell=True)

    print('Running {}'.format(yapf))
    subprocess.call(yapf, shell=True)


if __name__ == '__main__':
    manager.run()
