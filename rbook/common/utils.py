#!/usr/bin/env python
# encoding: utf-8

from flask import g
from models import app, db


def load_database():
    g.config = app.config
    g.database = db.load_database()
