# Copyright 2009 Alex K (wtwf.com) All rights reserved.

__author__ = 'wtwf.com (Alex K)'

import datetime
import logging
import random

from google.appengine.api import memcache
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.runtime import DeadlineExceededError

from lib.crud import crud_model

# used to prefix memcache keys to remember we missed something.
MISSING = 'Missing:'

class Snippy(crud_model.CrudNdbModel):
  keyword = ndb.StringProperty(required=True)
  url = ndb.TextProperty(required=True)
  alt_url = ndb.TextProperty()  # used when url has %s and no second param given
  mobile_url = ndb.TextProperty()  # used when requested form a mobile device
  suggest_url = ndb.TextProperty()  # used for suggest as you type
  suggest_jsonpath = ndb.TextProperty()  # used for suggest as you type
  private = ndb.BooleanProperty()
  proxy = ndb.BooleanProperty()
  promoted = ndb.BooleanProperty()
  used_count = ndb.IntegerProperty()
  created_date = ndb.DateTimeProperty(auto_now_add=True)

  def _pre_put_hook(self):
    memcache.delete(MISSING + self.keyword)

  @staticmethod
  def Search(query, request, response):
    arguments = request.arguments()

    if 'download' in arguments:
      response.headers['Content-Type'] = 'application/octet-stream'

    if 'keyword' in arguments:
      query = query.filter(Snippy.keyword == request.get('keyword'))
    else:
      if 'search' in arguments:
        search_param = request.get('search')

        # TODO(ark) make this do full text search https://cloud.google.com/appengine/docs/python/search/
        results = []
        try:
          for snip in query.iter():
            if search_param in snip.keyword or search_param in snip.url:
              if snip.keyword == search_param:
                results.insert(0, snip)
              else:
                results.append(snip)
        except DeadlineExceededError:
          logging.error('Ran out of time looking for: %r', search_param)
          pass
        return results
    return query

def GetByKeyword(kw):
  # see if this is in the not found memcache
  if memcache.get(MISSING + kw):
    logging.info('missing memcahe hit for %r', kw)
    return None
  try:
    ans = Snippy.query(Snippy.keyword == kw).get()
    if not ans:
      memcache.set(MISSING + kw, True, time=60 * 15)
    return ans
  except:
    return None


def NewRandomId():
  random.seed()
  letters = 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ0123456789'
  while True:
    kw = ''.join([random.choice(letters) for _ in range(0, 5)])
    # Make sure it doesn't exist
    if not GetByKeyword(kw):
      return kw
