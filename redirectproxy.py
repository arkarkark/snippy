# Copyright 2009 Alex K (wtwf.com) All rights reserved.

__author__ = 'wtwf.com (Alex K)'

import os
import urllib
import urllib2

from wtwf import wtwfhandler

PROXY_IMAGE_EXTENSIONS = ['.gif', '.png', '.jpg', '.jpeg']
REDIRECT_NORMALLY_EXTENSIONS = ['.xml', '.pdf']

class RedirectProxyHandler(wtwfhandler.WtwfHandler):

  def get(self, lookup):
    # first look in a url parameter
    url = self.request.get('url')
    # o.k. now look in the pathinfo and query_string
    if not url:
      url = urllib.unquote(lookup)
      if self.request.query_string:
        url += '?' + self.request.query_string
    ext = os.path.splitext(url)[1].lower()
    if ext in PROXY_IMAGE_EXTENSIONS:
      # fetch images and fake the referer
      try:
        req = urllib2.Request(url, headers={'referer': url})
        response = urllib2.urlopen(req)
        info = response.info()
        for header in ['Content-Type']:
          rh = info.getheader(header)
          if rh:
            self.response.headers[header] = rh
        self.response.out.write(response.read())
        return
      except:
        pass
    if ext in REDIRECT_NORMALLY_EXTENSIONS:
      self.redirect(str(url))
      return
    self.SendTemplate('redirect.html', dict(url=url))
