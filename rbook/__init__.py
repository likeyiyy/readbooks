#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.login import LoginManager
from flask_peewee.db import Database
from flask import rbg

from flask.ext.pagedown import PageDown


import os
import json

config_path = os.environ.get('READBOOK_CONFIG') or '/opt/web/config.json'
if os.path.exists(config_path):
    obj = json.loads(open(config_path).read())
    rbg.config = {}
    rbg.config.update(**obj)

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
pagedown = PageDown()
db = Database()


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'

def format_datetime(timestamp):
    """Format a timestamp for display."""
    return timestamp.strftime('%Y-%m-%d @ %H:%M')

def create_app():
    app = Flask(__name__)

    if os.path.exists(config_path):
        obj = json.loads(open(config_path).read())
        for key, value in obj.iteritems():
            if key.isupper():
                app.config[key] = value
    app.config.update(**app.config.get('MAIL'))

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)
    db.init_app(app)
    db.register_handlers()

    from werkzeug.wsgi import SharedDataMiddleware

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .book import book as book_blueprint
    app.register_blueprint(book_blueprint, url_prefix='/book')

    from .timeline import timeline as timeline_blueprint
    app.register_blueprint(timeline_blueprint, url_prefix='/timeline')

    app.jinja_env.filters['datetimeformat'] = format_datetime

    app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
        '/opt/web/upload': os.path.join(os.path.dirname(__file__), '/opt/web/upload')
    })

    return app


