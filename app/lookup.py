# Copyright 2009 Alex K (wtwf.com) All rights reserved.

__author__ = 'wtwf.com (Alex K)'

import urllib
import logging
import os

from google.appengine.api import users

import jinja2

from wtwf import wtwfhandler
import model
import snippy_config

__pychecker__ = 'no-override'

class SnippyHandler(wtwfhandler.WtwfHandler):

  def is_iPhone(self):
    ua = self.request.headers['User-Agent']
    for part in 'iPhone,AppleWebKit,Mobile/,Safari/,'.split(','):
      if part not in ua:
        return False
    return True

  def get(self, lookup, _):
    # Strip off the leading /
    path_info = lookup

    if not path_info:
      path_info = self.request.get('url')

    # look up the keyword
    snippy = model.GetByKeyword(path_info)
    url = None
    if snippy:
      url = self.GetUrl(snippy)
    else:
      if '%20' in path_info:
        path_info = urllib.unquote(path_info)
      elif '+' in path_info and self.is_iPhone():
        # friggin mobile safari and default search engines
        path_info = path_info.replace('+', ' ')

      # see if we have a space and then something
      parts = path_info.split(' ', 1)
      if len(parts) == 2:
        snippy = model.GetByKeyword(parts[0])
        if snippy:
          if self.request.query_string:
            parts[1] += '?' + self.request.query_string
          # TODO(ark): do we want to support {searchTerms} as well as %s?
          url = self.GetUrl(snippy).replace('%s',  urllib.quote(parts[1]))

    if snippy and '%s' in url and snippy.alt_url:
      url = snippy.alt_url

    if snippy:
      if snippy.private:
        if not users.is_current_user_admin():
          user = users.get_current_user()
          if user:
            url = None
          else:
            self.redirect(users.create_login_url(self.request.uri))
            return
      try:
        snippy.used_count = (snippy.used_count or 0) + 1
        snippy.put()
      except:
        logging.exception('unable to +1 counter for: %s (old counter %r)',
                          snippy.keyword, snippy.used_count)

    if url:
      if self.request.referrer:
        self.redirect('/r/' + urllib.quote(url.encode('utf-8')))
      else:
        # logging.info("No referrer so just using regular redirect")
        self.redirect(url.encode('utf-8'))
      return

    config = snippy_config.SnippyConfig()
    default_url = config.get('defaultUrl')
    if default_url:
      self.redirect(str(jinja2.Template(default_url).render({'url': lookup})))
    else:
      file_name = os.path.join(os.path.dirname(__file__), 'brand/default.html')
      file_contents = open(file_name).read()
      SEARCH = '<!--search-->'
      if users.is_current_user_admin():
        file_contents = file_contents.replace(
          SEARCH,
          '<link title="snippy" rel="search" type="application/opensearchdescription+xml" href="/admin/suggestxml">'
        )
      else:
        file_contents = file_contents.replace(
          SEARCH,
          '<!-- not admin -->'
        )

      self.response.out.write(file_contents)
