#!/usr/bin/env python
# encoding: utf-8

from rbook import create_app
from flask import g, current_app
from flask.ext.script import Manager, Shell
from flask_peewee.db import Database
from rbook.models import *
from rbook import create_app, db
from retry import retry
import requests
import traceback
import time
from bs4 import BeautifulSoup
app = create_app()

manager = Manager(app)
manager.add_command("shell", Shell())
s = requests.session()

def before_request():
    g.config = app.config
    g.database = db.load_database()

app.before_request(before_request)

@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

@manager.command
def create_tables():
    for klass in db.Model.__subclasses__():
        print klass._meta.db_table
        klass.create_table(fail_silently=True)


@manager.option('-m', '--model')
def create_table(model):
    klass = globals()[model]
    klass.create_table(fail_silently=True)

@manager.command
def init():
    create_tables()

headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36'
}


@retry(requests.exceptions.ConnectionError, tries=4, delay=3, backoff=2)
def connect_web(url):
    resp = s.get(url=url, headers=headers)
    return resp.text

_url = 'http://www.hbvjy.com/forum-126-{page}.html'

@manager.command
def marrygirl():
    current_page = 9
    total_page = 20
    while current_page <= total_page:
        start_url = _url.format(page=current_page)
        print 'current_page:{page}, url: {url}'.format(page=current_page, url=start_url)
        html = connect_web(url=start_url)
        soup = BeautifulSoup(html, "lxml")
        items = soup.findAll('tbody')
        results = []
        for item in items:
            try:
                id = item.get('id') or ''
                if 'normalthread' not in id:
                    continue

                title_url = item.find('th')
                author_date = item.find('td', class_='by')

                new_title = title_url.select('a[class*="xst"]')[0]
                title = new_title.text
                url = new_title['href']

                try:
                    address = title_url.em.a.text
                except AttributeError:
                    address = title

                author = author_date.cite.text
                date = author_date.em.text
                result = {
                    'title': title,
                    'url': url,
                    'author': author,
                    'address': address,
                    'dateAdded': date
                }
                if MarryGirl.select().where(MarryGirl.url == url).exists():
                    continue
                results.append(result)
            except:
                traceback.print_exc()
                import ipdb; ipdb.set_trace()

        if results:
            MarryGirl.insert_many(rows=results).execute()
        else:
            print 'not new insert'

        time.sleep(0.2)
        current_page += 1


if __name__ == "__main__":
    manager.run()
