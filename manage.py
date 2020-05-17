import os
import flask_migrate
from flask_script import Manager, Shell
from src.app import app, db
from src.models import Tender

basedir = os.path.abspath(os.path.dirname(__file__))
# app.config.from_object(app_config[configuration])
migrate = flask_migrate.Migrate(app, db)
manager = Manager(app)
manager.add_command("db", flask_migrate.MigrateCommand)


def make_shell_context():
    """
    :param:
    :return: application and database instances to the shell importing them automatically on python manager.py shell.
    """
    return dict(app=app, db=db, Tender=Tender)


manager.add_command("shell", Shell(make_context=make_shell_context))

if __name__ == '__main__':
    manager.run()