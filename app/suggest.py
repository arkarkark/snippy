# Copyright 2010 Alex K (wtwf.com) All rights reserved.

# useful?
# http://www.opensearch.org/Specifications/OpenSearch/Extensions/Suggestions/1.0
# http://www.opensearch.org/Specifications/OpenSearch/Extensions/Suggestions/1.1
# https://developer.mozilla.org/en-US/docs/Supporting_search_suggestions_in_search_plugins
"""
suggets reply is
```
[
  "imdb star wa",
  [
    "imdb Star Wars on IMDb",
    "imdb Solo: A Star Wars Story",
  ],
  [
    "Star Wars on IMDb",
    "Solo: A Star Wars Story",
  ],
  [
    "https://imdb.com/title//star-wars",
    "https://imdb.com/title/tt3778644",
  ]
]
```
"""
__author__ = 'wtwf.com (Alex K)'

import json
import logging
import os
import re
import urllib

import jsonpath_rw

import google.appengine.api.urlfetch

import jinja2

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
        url = snippy.suggest_url
        if '%s' in url:
          url = snippy.suggest_url.replace('%s', urllib.quote(parts[1]))
        elif '{{' in url:
          url = str(jinja2.Template(url).render({
            'searchTerms': urllib.quote(parts[1])
          }))
        elif '{searchTerms}' in url:
          url = snippy.suggest_url.replace('{searchTerms}', urllib.quote(parts[1]))
        # logging.info('loading: %r', url)
        res = google.appengine.api.urlfetch.fetch(url)
        reply = fixupSuggestReply(url, parts, res.content, snippy.suggest_jsonpath)
        self.response.headers['Content-Type'] = 'application/x-suggestions+json'
        # logging.info("REPLY\n%s", json.dumps(json.loads(reply), indent=2, sort_keys=True))
        self.response.out.write(reply)


class SuggestXmlHandler(wtwfhandler.WtwfHandler):
  def get(self):
    if os.getenv('SERVER_SOFTWARE', '').startswith('Google App Engine/'):
      dev = ''
    else:
      dev = '-dev'
    config = snippy_config.SnippyConfig()
    template_values = {
      'host': self.GetBaseUrl(),
      'shortName': config.get('shortName', 'shortName') + dev,
      'description': config.get('description', 'description') + dev,
      'developer': config.get('developer', 'developer') + dev,
    }
    self.response.headers['Content-Type'] = 'application/opensearchdescription+xml'
    self.SendTemplate('opensearch.xml', template_values)

def fixupGoogles(keyword, reply_key, reply):
  """the google.com/s format."""
  obj = getJson(reply)
  # the first element of arrays that are 4 deep
  choices = flatten(firstNdeep(obj, 4))
  choices = ['%s %s' % (keyword, x) for x in choices if isinstance(x, (str, unicode)) and x[-1] != '=']
  return json.dumps([reply_key, choices])

def FixupJsonPath(keyword, reply_key, reply, suggest_jsonpath):
  obj = json.loads(getJsonFromJsonP(reply))
  jsonpath_expr = jsonpath_rw.parse(suggest_jsonpath)
  obj = [
    reply_key,
    ['%s %s' % (keyword, x.value) for x in jsonpath_expr.find(obj)],
  ]
  return json.dumps(obj)

JSONP_START_RE = re.compile(r'^[a-zA-Z0-9_.]+\(', re.MULTILINE)
FIXUP_MAP = {
  r'^https://www\.google\.com/s\?tbm=': fixupGoogles,
}

def getJson(s):
  try:
    s = s[s.find('['):s.rfind(']') + 1]
    if s.find('[\\"') != -1:
      s = s.decode('string_escape') # google.com/s does this. Sends back a json string as a key to a dict.
  except e:
    pass
  return json.loads(s)

# ^^^ getJson is too agressive... use this soon...
def getJsonFromJsonP(s):
  json_pattern = re.compile(r"""^[^\(:;'"]*\((.*)\)""", re.MULTILINE)
  match = json_pattern.match(s)
  if match:
    return match.group(1)
  return s

def fixupSuggestReply(url, parts, reply, suggest_jsonpath=None):
  """Takes a suggest url reply and add the keyword to every suggestion."""
  keyword = parts[0]
  reply_key = ' '.join(parts)

  if suggest_jsonpath:
    return FixupJsonPath(keyword, reply_key, reply, suggest_jsonpath)
  else:
    for (regex, func) in FIXUP_MAP.items():
      if re.search(regex, url):
        return func(keyword, reply_key, reply)

  # make sure it's not jsonp
  obj = getJson(reply)

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
      for k in flatten(j):
        yield k
  else:
    if i:
      yield i

def firstNdeep(arr, depth, currentDepth=0):
  if not isinstance(arr, list):
    return None

  if depth == currentDepth:
    return arr[0]
  return [firstNdeep(x, depth, currentDepth + 1) for x in arr]
