#!/usr/bin/env python
# encoding: utf-8

from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
import peewee
from ..models import Book, UserBook, BookLabel, Label
from forms import BookForm
import datetime
import json

from . import book


def add_book(name, author, tags):
    now = datetime.datetime.now()
    tags = json.loads(tags)
    new_book = Book.select().filter(name=name, author=author).first()
    if new_book is None:
        new_book = Book(name=name,
                        author=author,
                        dateAdded=now,
                        lastUpdateDate=now)
        new_book.save()
        userbook_id = UserBook.insert(book=new_book.id,
                                      user=current_user.id,
                                      dateAdded=now,
                                      lastUpdateDate=now).execute()

        label_dicts = ({'name': tag, 'dateAdded': now} for tag in tags)
        Label.insert_many(label_dicts, upsert=True).execute()

        booklabel_dicts = ({'label': Label.get(name=tag),
                            'userbook': userbook_id,
                            'dateAdded': now,
                            'lastUpdateDate': now} for tag in tags)
        BookLabel.insert_many(booklabel_dicts, upsert=True).execute()
    else:
        try:
            UserBook.insert(book=new_book.id,
                            user=current_user.id,
                            dateAdded=now,
                            lastUpdateDate=now).execute()
        except peewee.IntegrityError:
            flash('You had already add this book.')



@book.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BookForm()
    if form.validate_on_submit():
        add_book(form.name.data,
                 form.author.data,
                 form.tags.data)
        flash('Book add now.')
        return redirect(url_for('main.index'))
    return render_template('book/add.html', form=form)



@book.route('/view/<bookname>')
@login_required
def view(bookname):
    return 'hello %s' % bookname

