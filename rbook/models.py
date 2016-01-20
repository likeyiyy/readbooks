#!/usr/bin/env python
# encoding: utf-8

from peewee import CharField, DateTimeField, BooleanField, ForeignKeyField, IntegerField
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask.ext.login import UserMixin, AnonymousUserMixin
from flask import current_app
from . import login_manager, db
import os

class User(UserMixin, db.Model):
    username = CharField(max_length=64, unique=True)
    email = CharField(unique=True)
    password_hash = CharField()
    confirmed = BooleanField(default=0)
    dateAdded = DateTimeField()
    lastUpdateDate = DateTimeField()

    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})


class Book(db.Model):
    name = CharField()
    author = CharField()
    contents_path = CharField()
    dateAdded = DateTimeField()
    lastUpdateDate = DateTimeField()

    class Meta:
        indexes = (
            (('name', 'author'), True),
        )

    def path(self, type, name, ext):
        return os.path.join('/opt/web/upload', type, name+'.'+ext)

    @property
    def contents(self):
        if not self.contents_path:
            self.contents_path = self.path('contents', self.name, 'jpg')
        return self.contents_path

    @contents.setter
    def contents(self, data):
        if not self.contents_path:
            self.contents_path = self.path('contents', self.name, 'jpg')
        with open(self.contents_path, 'wb') as fp:
            fp.write(data)



class Label(db.Model):
    name = CharField(unique=True)
    dateAdded = DateTimeField()

class UserBook(db.Model):
    user = ForeignKeyField(User, null=True)
    book = ForeignKeyField(Book, null=True)

    dateAdded = DateTimeField()
    lastUpdateDate = DateTimeField()

    class Meta:
        indexes = (
            (('user', 'book'), True),
        )


class BookLabel(db.Model):
    label = ForeignKeyField(Label)
    userbook = ForeignKeyField(UserBook)
    dateAdded = DateTimeField()
    lastUpdateDate = DateTimeField()

    class Meta:
        indexes = (
            (('label', 'userbook'), True),
        )

class GanDanText(db.Model):
    title = CharField()
    url = CharField()
    author = CharField()
    answer_number = IntegerField()
    dateAdded = DateTimeField()

class MarryGirl(db.Model):
    title = CharField()
    url = CharField()
    author = CharField()
    address = CharField()
    dateAdded = DateTimeField()

class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.select().filter(id=user_id).first()
