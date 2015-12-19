#!/usr/bin/env python
# encoding: utf-8


from flask import Blueprint

book = Blueprint('book', __name__)

from . import views
