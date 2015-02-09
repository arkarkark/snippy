"""Configuration settings for Snippy."""

import json
import os

class SnippyConfig(Object):
  """Config file reader for snippy parameters."""
  def __init__(self):
    file_name = os.path.join(os.path.dirname(__file__), 'brand/snippy_config.json')
    if os.path.exists(file_name):
      self.config = json.load(open(file_name))
    else:
      self.config = {}

  def get(self, key, default=None):
    """Get a config value."""
    return self.config.get(key, default)
