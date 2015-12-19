#!/usr/bin/env python
# encoding: utf-8

from rbook import create_app
from flask import g, current_app
from flask.ext.script import Manager, Shell
from flask_peewee.db import Database
from rbook import create_app, db

app = create_app()

manager = Manager(app)
manager.add_command("shell", Shell())


def before_request():
    g.config = app.config
    g.database = db.load_database()

app.before_request(before_request)

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
