#!/usr/bin/env python
# encoding: utf-8

from app import app
from models import db, User
from flask.ext.script import Manager, Shell

manager = Manager(app)

manager.add_command("shell", Shell())


@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def create_tables():
    for klass in db.Model.__subclasses__():
        print klass._meta.db_table
        klass.create_table(fail_silently=True)

@manager.command
def init():
    create_tables()


if __name__ == "__main__":
    manager.run()
