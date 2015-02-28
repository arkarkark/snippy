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

def fixupGoogles(keyword, reply_key, reply):
  """the google.com/s format."""
  obj = json.loads(getJson(reply))
  # the first element of arrays that are 4 deep
  choices = flatten(firstNdeep(obj, 4))
  choices = ['%s %s' % (keyword, x) for x in choices if isinstance(x, (str, unicode)) and x[-1] != '=']
  return json.dumps([reply_key, choices])


JSONP_START_RE = re.compile(r'^[a-zA-Z0-9_.]+\(', re.MULTILINE)
FIXUP_MAP = {
  r'^https://www\.google\.com/s\?tbm=': fixupGoogles
}

def getJson(s):
  try:
    s = s[s.find('['):s.rfind(']') + 1]
    if s.find('[\\"') != -1:
      s = s.decode('string_escape') # google.com/s does this. Sends back a json string as a key to a dict.
    return s
  except e:
    pass
  return s

def fixupSuggestReply(url, parts, reply):
  """Takes a suggest url reply and add the keyword to every suggestion."""
  keyword = parts[0]
  search_term = parts[1]
  reply_key = ' '.join(parts)

  for (regex, func) in FIXUP_MAP.items():
    if re.search(regex, url):
      return func(keyword, reply_key, reply)

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

def flatten(i):
  if isinstance(i, list) or isinstance(i, tuple):
    for j in i:
      for x in flatten(j):
        yield x
  else:
    if i:
      yield i

def firstNdeep(arr, depth, currentDepth=0):
  if not isinstance(arr, list):
    return None

  if depth == currentDepth:
    return arr[0]
  return [firstNdeep(x, depth, currentDepth + 1) for x in arr]
