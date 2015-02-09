import json
import os

class SnippyConfig:
  def __init__(self):
    file_name = os.path.join(os.path.dirname(__file__), 'static/snippy_config.json')
    if os.path.exists(file_name):
      self.config = json.load(open(file_name))
    else:
      self.config = {}

  def get(self, key):
    return self.config.get(key, key)
