# Copyright 2010 Alex K (wtwf.com) All rights reserved.

__author__ = 'wtwf.com (Alex K)'

import urllib
import logging
import re
import json

import google.appengine.api.urlfetch

from wtwf import wtwfhandler
import model
import snippy_config

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
        reply = fixupSuggestReply(url, parts, res.content)
        self.response.out.write(reply)


class SuggestXmlHandler(wtwfhandler.WtwfHandler):
  def get(self):
    config = snippy_config.SnippyConfig()
    template_values = {
      'host': self.GetBaseUrl(),
      'shortName': config.get('shortName', 'shortName'),
      'description': config.get('description', 'description'),
      'developer': config.get('developer', 'developer'),
    }
    xmltype = 'application/opensearchdescription+xml'
    self.response.headers['Content-Type'] = xmltype
    self.SendTemplate('opensearch.xml', template_values)

JSONP_START_RE = re.compile(r'^[a-zA-Z0-9_.]+\(', re.MULTILINE)
FIXUP_MAP = {}

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

def fixupSuggestReply(url, parts, reply):
  """Takes a suggest url reply and add the keyword to every suggestion."""
  keyword = parts[0]
  search_term = parts[1]
  reply_key = ' '.join(parts)

  # get domain of url
  url = getUrlHost(url)
  if url in FIXUP_MAP:
    return FIXUP_MAP[url](keyword, reply)

  # make sure it's not jsonp
  reply = getJson(reply)

  # first decode it
  obj = json.loads(reply)

  if len(obj) >= 2 and isinstance(obj[1], list):
    # result is ['searchTerm', ['option1', 'option2']]
    # fix up the search term in the result
    obj[0] = reply_key
    obj[1] = [fixupSuggestReplyEntry(keyword, x) for x in obj[1]]
  else:
    # assume result is ['option1', 'option2']
    obj = [reply_key, [fixupSuggestReplyEntry(keyword, x) for x in obj]]

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
