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
import user
import model
from lib.crud import crud_handler

class AHandler(webapp.RequestHandler):

  def get(self):
    self.response.out.write("hello world")

app = webapp.WSGIApplication([
  ('/admin/api/junk.*', AHandler),
  ('/admin/api/snip.*', crud_handler.GetCrudHandler(model.Snippy)),
  ('/admin/api/upload', upload.UploadHandler),
  ('/admin/api/user', user.UserHandler),
  ('/admin.old/add/(.*)', add.AddHandler),
  ('/admin.old/search.*', search.SearchHandler),
  ('/admin/suggestxml', suggest.SuggestXmlHandler),
  ('/admin/suggest', suggest.SuggestHandler),
  ('/r/(.*)', redirectproxy.RedirectProxyHandler),
  ('/((.|\n)*)', lookup.SnippyHandler),
])
