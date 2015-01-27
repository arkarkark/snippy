# Copyright 2009 Alex K (wtwf.com) All rights reserved.

__author__ = 'wtwf.com (Alex K)'

import json
import logging

from google.appengine.api import users
from google.appengine.ext import ndb

from wtwf import wtwfhandler
import model

class UploadHandler(wtwfhandler.WtwfHandler):

  @wtwfhandler.admin_required
  def get(self):
    self.AssertAllowed()
    template_values = {}
    self.redirect('/admin/import')

  def post(self):
    self.AssertAllowed()

    user = users.get_current_user()

    snip_file = self.request.POST.get('myfile').file
    logging.info('param: %r', snip_file)

    line = snip_file.readline()
    if line != ")]}',\n":
      snip_file.seek(0,0)

    snip_json = json.load(snip_file)
    logging.info('read a line: %r', line)


    logging.info('read some json: %r',
                 json.dumps(snip_json, sort_keys=True, indent=4, separators=(',', ': ')))

    snips = []
    for snip_json in snip_json:
      snip = model.Snippy(keyword='', url='')
      snip.UpdateFromJsonDict(snip_json)
      snips.append(snip)
      logging.info('made: %r', snip.keyword)

    ndb.put_multi(snips)

    self.redirect('/admin/import')
