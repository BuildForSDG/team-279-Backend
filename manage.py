#!/usr/bin/env python
import os
import flask_migrate
from flask_script import Manager, Shell
from app import app, db
from app.models import Tender, Company

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
def list_routes():
    import urllib

    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        output.append(line)

    for line in sorted(output):
        print(line)



if __name__ == '__main__':
    manager.run()
