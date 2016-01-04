#!/usr/bin/env python
# encoding: utf-8

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, \
    SubmitField, FileField, TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from flask.ext.pagedown.fields import PageDownField
from wtforms import ValidationError


class BookForm(Form):
    name = StringField(u'书名', validators=[DataRequired()])
    author = StringField(u'作者', validators=[DataRequired()])
    tags = StringField(u'标签', validators=[DataRequired()])
    contents = FileField(u'目录', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])
    submit = SubmitField('Add this book')


class BookView(Form):
    preface = TextAreaField(u'序言讲了什么？', validators=[DataRequired()])

