# Copyright 2009 Alex K (wtwf.com) All rights reserved.

__author__ = 'wtwf.com (Alex K)'

import json
import logging

from google.appengine.api import users
from google.appengine.ext import webapp

from lib.crud import crud_handler

import model
import well_known

import bouncer
import bouncer.constants as bc

@bouncer.authorization_method
def authorize(user, they):
  if users.is_current_user_admin():
    they.can(bc.MANAGE, bc.ALL)


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
        'can': {
          'editSnips': bouncer.can(user, bc.EDIT, model.Snippy),
          'editWellKnown': bouncer.can(user, bc.EDIT, well_known.WellKnown),
        },
        'logout': users.create_logout_url(url),
        'admin': users.is_current_user_admin(),
      }
    else:
      reply = {
        'login': users.create_login_url(url),
        'can': {},
      }

    self.response.headers['Content-Type'] = 'text/json'
    self.response.write(crud_handler.JSON_PREFIX + json.dumps(reply))
