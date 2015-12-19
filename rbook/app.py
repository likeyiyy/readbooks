#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask_peewee.db import Database
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.login import LoginManager
import json
import os
import datetime
app = Flask(__name__)
bootstrap = Bootstrap(app)
mail = Mail(app)
moment = Moment(app)

login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
config_path = os.environ.get('READBOOK_CONFIG') or '/opt/web/config.json'

if os.path.exists(config_path):
    obj = json.loads(open(config_path).read())
    for key, value in obj.iteritems():
        if key.isupper():
            app.config[key] = value

db = Database(app)
db.register_handlers()


def before_request():
    from common import utils
    utils.load_database()


def format_datetime(timestamp):
    """Format a timestamp for display."""
    return timestamp.strftime('%Y-%m-%d @ %H:%M')

app.jinja_env.filters['datetimeformat'] = format_datetime



