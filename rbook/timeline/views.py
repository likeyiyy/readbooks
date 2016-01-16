#!/usr/bin/env python
# encoding: utf-8

from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
import peewee
from ..models import Book, UserBook, BookLabel, Label
from forms import *
import datetime
import json
import uuid
from collections import OrderedDict
from . import timeline


@timeline.route('/view')
@login_required
def view():
    now = datetime.datetime.now()
    book = []
    for i in range(10):
        new_dict = {
            "id": i,
            "name": 'row' + str(i),
            "title": 'good',
            'uuid': str(uuid.uuid4()),
            'dateAdded': now
        }
        book.append(new_dict)
    keys = [
                "id",
                "name",
                "title",
                'uuid',
                'dateAdded'
            ]
    return render_template('timeline/view.html', keys=keys, book=book)
