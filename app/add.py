# Copyright 2009 Alex K (wtwf.com) All rights reserved.

__author__ = 'wtwf.com (Alex K)'

from wtwf import wtwfhandler
import model
import urllib
import logging

from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.api import urlfetch_errors

__pychecker__ = 'no-override'

class AddHandler(wtwfhandler.WtwfHandler):

  @wtwfhandler.admin_required
  def get(self, path):
    self.AssertAllowed()

    params = {}

    user = users.get_current_user()
    template_values = {'host': self.GetBaseUrl()}
    message = None

    path_info = urllib.unquote(path)
    parts = path_info.split(' ', 1)

    if len(parts) == 1:
      parts = [model.NewRandomId(), parts[0]]

    url = None
    kw = None
    alt_url = None
    mobile_url = None
    suggest_url = None

    if len(parts) == 2 and parts[1]:
      if not parts[1].startswith('http'):
        # perhaps it doesn't have a http and we need to add it.
        for a in  ('//', ':', 'http'):
          if not parts[1].startswith(a):
            parts[1] = a + parts[1]
        # parse the url and make sure the hostname resolves
        try:
          urlfetch.fetch(parts[1], allow_truncated=True, deadline=1)
        except urlfetch_errors.DownloadError, e:
          if 'nodename nor servname provided, or not known' in str(e):
            return self.Error('unfetchable url in "%s"', parts[1])

      kw = parts[0]
      url = parts[1]
      if self.request.query_string:
        url += '?' + self.request.query_string

    # TODO(ark) get it from request args
    if not kw:
      kw = self.request.get('keyword')
      url = self.request.get('url')
      alt_url = self.request.get('alt_url')
      mobile_url = self.request.get('mobile_url')
      suggest_url = self.request.get('suggest_url')

    if kw and url:
      orig = model.GetByKeyword(kw)
      if orig:
        if url and url != orig.url:
          params['url'] = url
      else:
        ns = model.Snippy(keyword=kw, url=url)
        try:
          ns.put()
        except:
          logging.exception('unable to add new snippy: %s', kw)
          return self.Error('Exception adding new snippy: %s', kw)

    params['keyword'] = kw
    self.redirect('/admin/edit/?%s' % urllib.urlencode(params))
