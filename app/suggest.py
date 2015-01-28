# Copyright 2010 Alex K (wtwf.com) All rights reserved.

__author__ = 'wtwf.com (Alex K)'

import urllib
import logging
import re
import json

import google.appengine.api.urlfetch

from wtwf import wtwfhandler
import model


class SuggestHandler(wtwfhandler.WtwfHandler):
  def get(self):
    q = self.request.get('q')
    parts = q.split(' ', 1)
    if len(parts) == 2:
      snippy = model.GetByKeyword(parts[0])
      if snippy and snippy.suggest_url:
        if snippy.private:
          self.AssertAllowed()
        parts[1] = parts[1].decode('utf-8')
        # TODO(ark): do we want to support {searchTerms} as well as %s?
        url = snippy.suggest_url.replace('%s', urllib.quote(parts[1]))
        res = google.appengine.api.urlfetch.fetch(url)
        self.response.out.write(fixupSuggestReply(url, parts[0], res.content))


class SuggestXmlHandler(wtwfhandler.WtwfHandler):
  def get(self):
    template_values = {'host': self.GetBaseUrl()}
    xmltype = 'application/opensearchdescription+xml'
    self.response.headers['Content-Type'] = xmltype
    self.SendTemplate('opensearch.xml', template_values)

def fixupUrbanDictionary(keyword, reply):
  reply = reply[reply.find('"') + 1:-1]
  reply = re.sub(r'\\u003C(/?strong|/?ul|/?span|li[^\\]*)\\u003E', '', reply)
  reply = reply.split('\u003C/li\u003E')
  if reply[-2] == 'more...':
    reply = reply[0:-2]
  reply = ['%s %s' % (keyword, reply[0]),
           ['%s %s' % (keyword, r) for r in reply[1:]]]
  return json.dumps(reply)

JSONP_START_RE = re.compile(r'^[a-zA-Z0-9_.]+\(', re.MULTILINE)
FIXUP_MAP = {'http://ajax.urbandictionary.com': fixupUrbanDictionary}

def getUrlHost(url):
  try:
    return url[0:url.find('/', 8)]
  except e:
    pass
  return url

def getJson(s):
  try:
    return s[s.find('['):s.rfind(']') + 1]
  except e:
    pass
  return s

def fixupSuggestReply(url, keyword, reply):
  """Takes a suggest url reply and add the keyword to every suggestion."""
  # get domain of url
  url = getUrlHost(url)
  print url
  if url in FIXUP_MAP:
    return FIXUP_MAP[url](keyword, reply)

  # make sure it's not jsonp
  reply = getJson(reply)

  # first decode it
  obj = json.loads(reply)
  # fix up the search term in the result
  obj[0] = keyword + ' ' + obj[0]
  # then fix up each result
  obj[1] = [fixupSuggestReplyEntry(keyword, x) for x in obj[1]]
  # then reencode it and send it back
  return json.dumps(obj)

def fixupSuggestReplyEntry(keyword, entry):
  if isinstance(entry, basestring):
    return keyword + ' ' + removeBold(entry)
  else:
    return keyword + ' ' + removeBold(entry[0])



BOLD_RE = re.compile(r'(\u003C/?b\u003E|</?b>)', re.MULTILINE)

def removeBold(entry):
  return BOLD_RE.sub('', entry)
