# Copyright 2018 Alex K (wtwf.com) All rights reserved.

"""
Find the search url (and the suggest url) for a site
gold standard (even if it's php and downloads the file)

http://www.gutenberg.org/
http://www.gutenberg.org/w/opensearch_desc.php
http://www.gutenberg.org/w/api.php?action=opensearch&search=arctic&namespace=0|4

also should support ld+json (doesn't seem to have suggest support)
https://developers.google.com/search/docs/data-types/sitelinks-searchbox

https://www.chewy.com/

other sites:
https://www.costco.com/
https://www.airbnb.com/opensearch.xml
https://www.crunchbase.com/opensearch.xml?version=2
https://www.labnol.org/
https://www.diigo.com/search/open_search
https://community.dremio.com/
https://domains.google/#/
https://earlyretirementnow.com/osd.xml
https://www.flickr.com/opensearch.xml

"""

__author__ = 'wtwf.com (Alex K)'

import json
import logging
import re
import urlparse
import HTMLParser
import xml.etree.ElementTree

import google.appengine.api.urlfetch

from wtwf import wtwfhandler


class FindHrefParser(HTMLParser.HTMLParser):

  def reset(self):
    HTMLParser.HTMLParser.reset(self)
    self.hrefs = []

  def handle_starttag(self, tag, attrs):
    if 'href' in attrs:
      self.hrefs.append(attrs['href'])


class FindOpensearchHandler(wtwfhandler.WtwfHandler):

  def get(self):
    url = self.request.get('url')
    base = urlparse.urljoin(url, '/')

    res = google.appengine.api.urlfetch.fetch(base)

    content = res.content

    # first try and find opensearch
    opensearch_re = re.compile(r'<[^>]*opensearchdescription\+xml[^>]*>')
    match = opensearch_re.search(content)
    if match:
      parser = FindHrefParser()
      parser.feed(match.group(0))
      if len(parser.hrefs) > 0:
        href = parser.hrefs[0]
        res = google.appengine.api.urlfetch.fetch(urlparse.urljoin(base, href))
        content = res.content
        # xml parse that shit
        root = xml.etree.ElementTree.fromstring(content)
        # get the Url elements (url, URL too)

        # if it's text/html it's the search url, get template, replace {searchTerms} with %s
        # make sure it doesn't have &amp;

        # if it's application/x-suggestions+json then it's the suggest url

        # if it only has application/x-suggestions+xml then that's messed up


    # second try and find ld+json
