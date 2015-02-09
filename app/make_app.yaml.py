#!/usr/bin/python

# you could try this too... `sudo pip install Jinja2`
import site
site.addsitedir('/usr/local/google_appengine/lib/jinja2-2.6/')

import os
import jinja2

import snippy_config

def Main():
  """Make an app.yaml file."""
  config = snippy_config.SnippyConfig()
  in_file = open(os.path.join(os.path.dirname(__file__), 'app_template.yaml')).read()
  out_file = open(os.path.join(os.path.dirname(__file__), 'app.yaml'), 'w')
  out_file.write(jinja2.Template(in_file).render({
    'application': config.get('application', 'snippy'),
    'version': config.get('version', '1'),
  }))

if __name__ == '__main__':
  Main()
