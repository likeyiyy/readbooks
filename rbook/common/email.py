from threading import Thread
from flask.ext.mail import Message, Mail
from views import app
from flask import render_template

app.config.update(**app.config.get('MAIL'))
mail = Mail(app)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    msg = Message(app.config['ReadBook_MAIL_SUBJECT_PREFIX'] + ' ' + subject,
                  sender=app.config['ReadBook_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr
