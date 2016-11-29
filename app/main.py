# Copyright 2009 Alex K (wtwf.com) All rights reserved.

"""Snippy a short url app engine thing (and more!)."""

__author__ = 'wtwf.com (Alex K)'

# If you want to check this with pychecker on osx you can do this...
# export PYTHONPATH=/usr/local/google_appengine/:/usr/local/google_appengine/lib/yaml/lib/:$PYTHONPATH

from google.appengine.ext import webapp

import add
import import_snips
import lookup
import model
import redirectproxy
import snippy_config_handler
import suggest
import user
from lib.crud import crud_handler

app = webapp.WSGIApplication([
  ('/admin/api/snippyconfig.*', snippy_config_handler.SnippyConfigHandler),
  ('/admin/api/snip.*', crud_handler.GetCrudHandler(model.Snippy)),
  ('/admin/api/import', import_snips.ImportHandler),
  ('/admin/api/user', user.UserHandler),
  ('/admin/add/(.*)', add.AddHandler),
  ('/admin/suggestxml', suggest.SuggestXmlHandler),
  ('/admin/suggest.*', suggest.SuggestHandler),
  ('/r/(.*)', redirectproxy.RedirectProxyHandler),
  ('/((.|\n)*)', lookup.SnippyHandler),
])
