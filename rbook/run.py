#!/usr/bin/env python
# encoding: utf-8

from _views import app
from book import book
app.register_blueprint(book, url_prefix='book')

app.run(debug=True, port=8001)
