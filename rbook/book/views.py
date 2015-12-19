#!/usr/bin/env python
# encoding: utf-8

from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
import peewee
from ..models import Book, UserBook
from forms import BookForm
import datetime

from . import book


@login_required
@book.route('/add', methods=['GET','POST'])
def add():
    form = BookForm()
    if form.validate_on_submit():
        now = datetime.datetime.now()
        new_book = Book.select().filter(name=form.name.data, author=form.author.data).first()
        if new_book is None:
            new_book = Book(name=form.name.data,
                            author=form.author.data,
                            dateAdded=now,
                            lastUpdateDate=now)
            new_book.save()
            UserBook.insert(book=new_book.id,
                            user=current_user.id,
                            dateAdded=now,
                            lastUpdateDate=now).execute()

        else:
            try:
                UserBook.insert(book=new_book.id,
                                user=current_user.id,
                                dateAdded=now,
                                lastUpdateDate=now).execute()
            except peewee.IntegrityError:
                flash('You had already add this book.')

        flash('Book add now.')
        return redirect(url_for('main.index'))
    return render_template('book/add.html', form=form)

@book.route('/book/<bookname>')
def view(bookname):
    return 'hello %s' % bookname

