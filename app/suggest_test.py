#!/usr/bin/python
# Copyright 2010 Alex K (wtwf.com) All rights reserved.

# export PYTHONPATH=

import sys

sys.path.append('/usr/local/google_appengine/')
sys.path.append('/usr/local/google_appengine/lib/yaml/lib/')
sys.path.append('/usr/local/google_appengine/lib/webob-1.2.3/')
sys.path.append('/usr/local/google_appengine/lib/django-1.3')

from google.appengine.dist import use_library
use_library('django', '1.3')

import json
import suggest
import unittest

class TextSuggest(unittest.TestCase):

  def testfixupSuggestReply(self):
    tests = [
      ('http://suggest.google.com/something',
       ['g', 'flower'],
       '["flower",["http:\\/\\/www.1800flowers.com\\/","flowers","flower delivery","flower girl dresses"],["Flowers, Roses, Gift Baskets, Flower Bouquets - 1-800-FLOWERS.COM","165,000,000 results","15,600,000 results","7,080,000 results"],[],{"google:suggesttype":["NAVIGATION","QUERY","QUERY","QUERY"]}]',
       '["g flower",["g http:\\/\\/www.1800flowers.com\\/","g flowers","g flower delivery","g flower girl dresses"],["Flowers, Roses, Gift Baskets, Flower Bouquets - 1-800-FLOWERS.COM","165,000,000 results","15,600,000 results","7,080,000 results"],[],{"google:suggesttype":["NAVIGATION","QUERY","QUERY","QUERY"]}]'),
      ('http://news.google.com/complete/search?hl=en&gl=us&ds=n&nolabels=t&hjson=t&q=tyl',
       ['gn', 'tyl'],
       '["tyl",[["tyler grady","0"],["tyler hansbrough","1"],["tyler perry","2"],["tylenol","3"],["tylenol recall","4"],["tylenol recall 2010","5"],["tyler grady american idol","6"],["tyler thigpen","7"],["tyler weinman","8"],["tyler ramaker","9"]]]',
       '["gn tyl",["gn tyler grady","gn tyler hansbrough","gn tyler perry","gn tylenol","gn tylenol recall","gn tylenol recall 2010","gn tyler grady american idol","gn tyler thigpen","gn tyler weinman","gn tyler ramaker"]]'),
      ('http://clients1.google.com/complete/search?hl=en&client=img&expIds=17259&ds=i&q=fish&cp=6',
       ['gis', 'fish'],
       'window.google.ac.h(["fish",[["fish\u003Cb\u003E pictures\u003C\/b\u003E",0,"0"],["fish\u003Cb\u003Eing\u003C\/b\u003E",0,"1"],["fish\u003Cb\u003Ey\u003C\/b\u003E",0,"2"],["fish\u003Cb\u003Ees\u003C\/b\u003E",0,"3"],["fish\u003Cb\u003E and chips\u003C\/b\u003E",0,"4"],["fish\u003Cb\u003E tank\u003C\/b\u003E",0,"5"],["fish\u003Cb\u003E clip art\u003C\/b\u003E",0,"6"],["fish\u003Cb\u003Eerman\u003C\/b\u003E",0,"7"],["fish\u003Cb\u003Eer cat\u003C\/b\u003E",0,"8"],["fish\u003Cb\u003Eing boat\u003C\/b\u003E",0,"9"]]])',
       '["gis fish", ["gis fish pictures", "gis fishing", "gis fishy", "gis fishes", "gis fish and chips", "gis fish tank", "gis fish clip art", "gis fisherman", "gis fisher cat", "gis fishing boat"]]'),

      # http://completion.amazon.com/search/complete?method=completion&q=%s&search-alias=aps&client=amazon-search-ui&mkt=1&x=updateISSCompletion&sc=1&noCacheIE=1272854187151
      ('http://api.urbandictionary.com/v0/autocomplete?key=ab71d33b15d36506acf1e379b0ed07ee&term=target',
       ['urban', 'target'],
       '["target","target cart attendant","target rich environment","targeted individual","target farting","target tattoo","target confusion","target finder","target misdirect","target whore"]',
       '["urban target", ["urban target","urban target cart attendant","urban target rich environment","urban targeted individual","urban target farting","urban target tattoo","urban target confusion","urban target finder","urban target misdirect","urban target whore"]]'),
      ]

    for url, parts, reply, expected in tests:
      print "KEYWORD: " + ' '.join(parts)
      self.assertEqual(json.dumps(json.loads(expected)),
                       suggest.fixupSuggestReply(url, parts, reply))

if __name__ == '__main__':
    unittest.main()
