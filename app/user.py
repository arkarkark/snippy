# Copyright 2009 Alex K (wtwf.com) All rights reserved.

__author__ = 'wtwf.com (Alex K)'

import json
import logging



from google.appengine.api import users
from google.appengine.ext import webapp

from lib.crud import crud_handler

class UserHandler(webapp.RequestHandler):

  def get(self):
    url = self.request.get('url') or self.request.referer or '/'
    user = users.get_current_user()
    if user:
      reply = {
        'nickname': user.nickname(),
        'email': user.email(),
        'user_id': user.user_id(),
        'federated_identity': user.federated_identity(),
        'federated_provider': user.federated_provider(),
        'can': {},
      }
    else:
      reply = {
        'login': users.create_login_url(url),
        'can': {},
      }

    self.response.headers['Content-Type'] = 'text/json'
    self.response.write(crud_handler.JSON_PREFIX + json.dumps(reply))
