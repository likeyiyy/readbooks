#!/usr/bin/env python
# encoding: utf-8

from app import app
from forms import *
from models import *
from flask import render_template, g, session, flash, redirect, url_for, request
from flask.ext.moment import Moment
from flask.ext.login import current_user, login_user, logout_user, login_required
from common.email import send_email
import datetime

moment = Moment(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.select().filter(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            user.lastUpdateDate = datetime.datetime.now()
            login_user(user, form.remember_me.data)
            user.save()
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid emailname or password.')
    return render_template('auth/login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('index'))


@app.route('/user')
def user():
    return 'hello world'



@app.route('/signup', methods=['GET', 'POST'])
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
        return redirect(url_for('login'))
    return render_template('auth/register.html', form=form)


@app.route('/confirm/<token>')
@login_required
def confirm(token):
    if g.user.confirmed:
        return redirect(url_for('index'))
    if g.user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('index'))



