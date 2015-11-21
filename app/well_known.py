# Copyright 2015 Alex K (wtwf.com) All rights reserved.

"""handlers to set and serve .well-known stuff for letsencrypt."""
__author__ = 'wtwf.com (Alex K)'

import json
import logging

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import ndb

class WellKnown(ndb.Model):
  url = ndb.StringProperty(required=True)
  fact = ndb.StringProperty(required=True)

class WellKnownPublicHandler(webapp.RequestHandler):

  def get(self, url):
    logging.info("requesting fact: %r", url)
    ans = WellKnown.query(WellKnown.url == url).get()
    if ans is not None:
      self.response.out.write(ans.fact)
    else:
      self.error(404)



class WellKnownAdminHandler(webapp.RequestHandler):

  def post(self):
    user = users.get_current_user()
    if not users.is_current_user_admin():
      self.error(403)
      return
    req = json.loads(self.request.body)
    logging.info("yay %r", req['fact'])
    fact = req['fact']
    well_known = WellKnown(
      url=fact.split(".")[0],
      fact=fact
    ).put()

    self.response.headers['Content-Type'] = 'text/json'
    self.response.out.write(json.dumps({"status": "success"}))
