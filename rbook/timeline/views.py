#!/usr/bin/env python
# encoding: utf-8

from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
import peewee
from ..models import *
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

@timeline.route('/gandan')
@login_required
def gandan_view():
    titles = [u'标题', u'作者', u'回复数', u'添加日期']
    lists = GanDanText.select().order_by(-GanDanText.answer_number).limit(100)
    return render_template('timeline/gandan.html', lists=lists, titles=titles)


@timeline.route('/marrygirl')
@login_required
def marrygirl():
    titles = [u'标题', u'作者', u'地址', u'添加日期']
    lists = MarryGirl.select().where(MarryGirl.address == u'河南省').order_by(-MarryGirl.dateAdded).limit(200)
    return render_template('timeline/marrygirl.html', lists=lists, titles=titles)
