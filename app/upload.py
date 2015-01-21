# Copyright 2009 Alex K (wtwf.com) All rights reserved.

__author__ = 'wtwf.com (Alex K)'

import ConfigParser
import StringIO

from google.appengine.api import users

from wtwf import wtwfhandler
import model

class UploadHandler(wtwfhandler.WtwfHandler):

  @wtwfhandler.admin_required
  def get(self):
    self.AssertAllowed()
    template_values = {}
    self.SendTemplate('upload.html', {})

  def post(self):
    self.AssertAllowed()

    user = users.get_current_user()

    snipdb = self.request.get('myfile')
    config = ConfigParser.ConfigParser()

    snipdb_file = StringIO.StringIO(snipdb)

    config.readfp(snipdb_file)
    urls = []
    if config.has_section('urls'):
      for key, url in config.items('urls'):
        url = url.strip('"')
        u = model.GetByKeyword(key)
        if (u):
          status = 'already'
        else:
          try:
            ns = model.Snippy(keyword=key, url=url, owner=user)
            ns.put()
            status = 'added'
          except:
            status = 'failed:'

        urls.append(dict(keyword=key, url=url, status=status))
    self.SendTemplate('import.html', dict(urls=urls))
