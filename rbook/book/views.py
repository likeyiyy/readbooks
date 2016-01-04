#!/usr/bin/env python
# encoding: utf-8

from flask import render_template, redirect, request, url_for, flash
from flask.ext.login import login_user, logout_user, login_required, current_user
import peewee
from ..models import Book, UserBook, BookLabel, Label
from forms import BookForm, BookView
import datetime
import json

from . import book


def add_book(name, author, tags, contents):
    now = datetime.datetime.now()
    tags = json.loads(tags)
    new_book = Book.select().filter(name=name, author=author).first()
    if new_book is None:
        new_book = Book(name=name,
                        author=author,
                        dateAdded=now,
                        lastUpdateDate=now)
        new_book.contents = contents
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
        contents = form.contents.data.stream.read()
        add_book(form.name.data,
                 form.author.data,
                 form.tags.data,
                 contents)
        flash('Book add now.')
        return redirect(url_for('book.view', bookname=form.name.data))
    return render_template('book/add.html', form=form)



@book.route('/view/<bookname>')
@login_required
def view(bookname):
    try:
        book = Book.get(name=bookname)
        userbook = UserBook.get(book=book.id, user=current_user.id)
        labels = Label.select().filter(id__in=BookLabel.select(BookLabel.label)
                                                       .filter(userbook=userbook.id))
        for label in labels:
            print label.name
        book.tags = labels
    except:
        book = None
    form = BookView()
    return render_template('book/view.html', form=form, book=book)

