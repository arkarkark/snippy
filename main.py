# Copyright 2009 Alex K (wtwf.com) All rights reserved.

__author__ = 'wtwf.com (Alex K)'

# If you want to check this with pychecker on osx you can do this...
# export PYTHONPATH=/usr/local/google_appengine/:/usr/local/google_appengine/lib/yaml/lib/:$PYTHONPATH

from google.appengine.ext import webapp

import add
import lookup
import redirectproxy
import search
import suggest
import upload

app = webapp.WSGIApplication([
    ('/admin/upload', upload.UploadHandler),
    ('/admin/add/(.*)', add.AddHandler),
    ('/admin/search.*', search.SearchHandler),
    ('/admin/suggestxml', suggest.SuggestXmlHandler),
    ('/admin/suggest', suggest.SuggestHandler),
    ('/r/(.*)', redirectproxy.RedirectProxyHandler),
    ('/((.|\n)*)', lookup.SnippyHandler),
    ])
