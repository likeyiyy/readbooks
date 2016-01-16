#!/usr/bin/env python
# encoding: utf-8

from flask import Blueprint

timeline = Blueprint('timeline', __name__)

from . import views

