#!/usr/bin/env python
# encoding: utf-8

from forms import *
from ..models import User, UserBook
from flask import render_template, g, flash, redirect, url_for, request
from flask.ext.login import current_user, login_user, logout_user, login_required
from rbook.common.email import send_email
import datetime
from . import main

@main.route('/')
def index():
    books = UserBook.select().filter(user=current_user)
    return render_template('index.html', books=books)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.select().filter(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            user.lastUpdateDate = datetime.datetime.now()
            login_user(user, form.remember_me.data)
            user.save()
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid emailname or password.')
    return render_template('auth/login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@main.route('/user/<username>')
def user(username):
    return 'hello %s' % username


@main.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.username = form.username.data
        user.email = form.email.data
        user.dateAdded = datetime.datetime.now()
        user.password = form.password.data
        user.lastUpdateDate = datetime.datetime.now()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Confirm Your Account',
                   'auth/email/confirm', user=user, token=token)
        flash('A confirmation email has been sent to you by email.')
        user.save()
        return redirect(url_for('main.login'))
    return render_template('auth/register.html', form=form)


@main.route('/confirm/<token>')
@login_required
def confirm(token):
    if g.user.confirmed:
        return redirect(url_for('main.index'))
    if g.user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))






