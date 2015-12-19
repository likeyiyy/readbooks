#!/usr/bin/env python
# encoding: utf-8

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.login import LoginManager
from flask_peewee.db import Database
import os
import json
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'main.login'

config_path = os.environ.get('READBOOK_CONFIG') or '/opt/web/config.json'


def create_app():
    app = Flask(__name__)

    if os.path.exists(config_path):
        obj = json.loads(open(config_path).read())
        for key, value in obj.iteritems():
            if key.isupper():
                app.config[key] = value

    db = Database(app)
    db.register_handlers()

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .book import book as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/book')

    return app


