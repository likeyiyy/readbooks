#!/usr/bin/env python
# encoding: utf-8

from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError


class BookForm(Form):
    name = StringField('What is this book name?', validators=[DataRequired()])
    author = StringField('What is this book author?', validators=[DataRequired()])
    submit = SubmitField(u'添加')

