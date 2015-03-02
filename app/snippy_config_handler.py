# Copyright 2015 Alex K (wtwf.com) All rights reserved.

__author__ = 'wtwf.com (Alex K)'

import json
import logging
import urllib

from wtwf import wtwfhandler
import snippy_config

__pychecker__ = 'no-override'

class SnippyConfigHandler(wtwfhandler.WtwfHandler):

  def get(self):
    config = snippy_config.SnippyConfig()
    logging.info('url %r', self.request.url)
    self.response.write(json.dumps({
      'baseUrl': config.get('baseUrl', self.GetBaseUrl() + '/'),
    }))
