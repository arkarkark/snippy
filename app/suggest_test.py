#!/usr/bin/python
# Copyright 2010 Alex K (wtwf.com) All rights reserved.

# export PYTHONPATH=/usr/local/google_appengine/:/usr/local/google_appengine/lib/yaml/lib/:/usr/local/google_appengine/lib/webob/:/usr/local/google_appengine/lib/django/:$PYTHONPATH

import unittest

from django.utils import simplejson
import suggest

class TextSuggest(unittest.TestCase):

  def testfixupSuggestReply(self):
    tests = [
      ("http://suggest.google.com/something",
       "g",
       """["flower",["http:\\/\\/www.1800flowers.com\\/","flowers","flower delivery","flower girl dresses"],["Flowers, Roses, Gift Baskets, Flower Bouquets - 1-800-FLOWERS.COM","165,000,000 results","15,600,000 results","7,080,000 results"],[],{"google:suggesttype":["NAVIGATION","QUERY","QUERY","QUERY"]}]""",
       """["g flower",["g http:\\/\\/www.1800flowers.com\\/","g flowers","g flower delivery","g flower girl dresses"],["Flowers, Roses, Gift Baskets, Flower Bouquets - 1-800-FLOWERS.COM","165,000,000 results","15,600,000 results","7,080,000 results"],[],{"google:suggesttype":["NAVIGATION","QUERY","QUERY","QUERY"]}]"""),
      ("http://news.google.com/complete/search?hl=en&gl=us&ds=n&nolabels=t&hjson=t&q=tyl",
       "gn",
       """["tyl",[["tyler grady","0"],["tyler hansbrough","1"],["tyler perry","2"],["tylenol","3"],["tylenol recall","4"],["tylenol recall 2010","5"],["tyler grady american idol","6"],["tyler thigpen","7"],["tyler weinman","8"],["tyler ramaker","9"]]]""",
       """["gn tyl",["gn tyler grady","gn tyler hansbrough","gn tyler perry","gn tylenol","gn tylenol recall","gn tylenol recall 2010","gn tyler grady american idol","gn tyler thigpen","gn tyler weinman","gn tyler ramaker"]]"""),
      ("http://clients1.google.com/complete/search?hl=en&client=img&expIds=17259&ds=i&q=fish&cp=6",
       "gis",
       """window.google.ac.h(["fish",[["fish\u003Cb\u003E pictures\u003C\/b\u003E",0,"0"],["fish\u003Cb\u003Eing\u003C\/b\u003E",0,"1"],["fish\u003Cb\u003Ey\u003C\/b\u003E",0,"2"],["fish\u003Cb\u003Ees\u003C\/b\u003E",0,"3"],["fish\u003Cb\u003E and chips\u003C\/b\u003E",0,"4"],["fish\u003Cb\u003E tank\u003C\/b\u003E",0,"5"],["fish\u003Cb\u003E clip art\u003C\/b\u003E",0,"6"],["fish\u003Cb\u003Eerman\u003C\/b\u003E",0,"7"],["fish\u003Cb\u003Eer cat\u003C\/b\u003E",0,"8"],["fish\u003Cb\u003Eing boat\u003C\/b\u003E",0,"9"]]])""",
       """["gis fish", ["gis fish pictures", "gis fishing", "gis fishy", "gis fishes", "gis fish and chips", "gis fish tank", "gis fish clip art", "gis fisherman", "gis fisher cat", "gis fishing boat"]]"""),

      # http://completion.amazon.com/search/complete?method=completion&q=%s&search-alias=aps&client=amazon-search-ui&mkt=1&x=updateISSCompletion&sc=1&noCacheIE=1272854187151
      ("http://ajax.urbandictionary.com/autocomplete.php?term=f&revision=6313&callback=_prototypeJSONPCallback_1",
       "urban",
       """_prototypeJSONPCallback_1("\u003Cul\u003E\u003Cli\u003E\u003Cspan\u003E\u003Cstrong\u003Ef\u003C/strong\u003E\u003C/span\u003E\u003C/li\u003E\u003Cli\u003E\u003Cspan\u003E\u003Cstrong\u003Ef\u003C/strong\u003Eacebook\u003C/span\u003E\u003C/li\u003E\u003Cli\u003E\u003Cspan\u003E\u003Cstrong\u003Ef\u003C/strong\u003Etw\u003C/span\u003E\u003C/li\u003E\u003Cli\u003E\u003Cspan\u003E\u003Cstrong\u003Ef\u003C/strong\u003Eo' shizzle my nizzle\u003C/span\u003E\u003C/li\u003E\u003Cli\u003E\u003Cspan\u003E\u003Cstrong\u003Ef\u003C/strong\u003Erance\u003C/span\u003E\u003C/li\u003E\u003Cli\u003E\u003Cspan\u003E\u003Cstrong\u003Ef\u003C/strong\u003Eaggot\u003C/span\u003E\u003C/li\u003E\u003Cli\u003E\u003Cspan\u003E\u003Cstrong\u003Ef\u003C/strong\u003Eugly\u003C/span\u003E\u003C/li\u003E\u003Cli\u003E\u003Cspan\u003E\u003Cstrong\u003Ef\u003C/strong\u003Eap\u003C/span\u003E\u003C/li\u003E\u003Cli\u003E\u003Cspan\u003E\u003Cstrong\u003Ef\u003C/strong\u003Eart\u003C/span\u003E\u003C/li\u003E\u003Cli\u003E\u003Cspan\u003E\u003Cstrong\u003Ef\u003C/strong\u003Eox news\u003C/span\u003E\u003C/li\u003E\u003Cli id=\"more\"\u003E\u003Cspan\u003Emore...\u003C/span\u003E\u003C/li\u003E\u003C/ul\u003E")""",
       """["urban f", ["urban facebook", "urban ftw", "urban fo\' shizzle my nizzle", "urban france", "urban faggot", "urban fugly", "urban fap", "urban fart", "urban fox news"]]""")
      ]

    for url, keyword, reply, expected in tests:
      print "KEYWORD: " + keyword
      self.assertEqual(simplejson.dumps(simplejson.loads(expected)),
                       suggest.fixupSuggestReply(url, keyword, reply))

if __name__ == '__main__':
    unittest.main()
