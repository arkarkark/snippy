# Copyright 2009 Alex K (wtwf.com) All rights reserved.

__author__ = 'wtwf.com (Alex K)'

from wtwf import wtwfhandler
import model
import urllib
import logging

from google.appengine.api import users
from google.appengine.api import urlfetch
from google.appengine.api import urlfetch_errors

__pychecker__ = 'no-override'

class AddHandler(wtwfhandler.WtwfHandler):

  @wtwfhandler.admin_required
  def get(self, path):
    self.AssertAllowed()
    self.post(path)

  def post(self, path):
    self.AssertAllowed()

    user = users.get_current_user()
    template_values = {'host': self.GetBaseUrl()}
    message = None

    path_info = urllib.unquote(path)
    parts = path_info.split(' ', 1)

    if len(parts) == 1:
      parts = [model.NewRandomId(), parts[0]]

    url = None
    kw = None
    alt_url = None
    mobile_url = None
    suggest_url = None

    if len(parts) == 2 and parts[1]:
      if not parts[1].startswith('http'):
        # perhaps it doesn't have a http and we need to add it.
        for a in  ('//', ':', 'http'):
          if not parts[1].startswith(a):
            parts[1] = a + parts[1]
        # parse the url and make sure the hostname resolves
        try:
          urlfetch.fetch(parts[1], allow_truncated=True, deadline=1)
        except urlfetch_errors.DownloadError, e:
          if 'nodename nor servname provided, or not known' in str(e):
            return self.Error('unfetchable url in "%s"', parts[1])

      kw = parts[0]
      url = parts[1]
      if self.request.query_string:
        url += '?' + self.request.query_string

    private = None
    private = self.request.get('private', None)
    if private is not None:
      private = private == 'yes'

    # TODO(ark) get it from request args
    if not kw:
      kw = self.request.get('keyword')
      url = self.request.get('url')
      alt_url = self.request.get('alt_url')
      mobile_url = self.request.get('mobile_url')
      suggest_url = self.request.get('suggest_url')

    action = 'submit'
    if kw and url:
      orig = model.GetByKeyword(kw)
      if orig:
        if self.request.get('submit') == 'delete':
          message = ('keyword "%s" deleted\n'
                     '(you can recreate it below if you like)' % kw)
          orig.key.delete()
          action = 'create'
        elif self.request.get('submit') in ('replace', 'update'):
          changed = []
          if url and url != orig.url:
            orig.url = url
            changed.append('url')
          if alt_url and alt_url != orig.alt_url:
            orig.alt_url = alt_url
            changed.append('alternate url')
          if mobile_url and mobile_url != orig.mobile_url:
            orig.mobile_url = mobile_url
            changed.append('mobile url')
          if suggest_url and suggest_url != orig.suggest_url:
            orig.suggest_url = suggest_url
            changed.append('suggest url')
          if private is not None and private != orig.private:
            orig.private = private
            changed.append((private and 'private') or 'public')

          if changed:
            # TODO(ark): orig.private =
            try:
              orig.put()
            except:
              logging.exception('unable to add new snippy: %s', orig.keyword)
              return self.Error('Exception updating snippy: %s', orig.keyword)

            message = '%s Updated for "%s"' % (', '.join(changed), kw)
            action = 'update'
          else:
            message = 'no change'
            action = 'replace'
        else:
          message = 'keyword already exists! "%s"' % kw
          if orig.url != url:
            template_values['orig_url'] = orig.url
          template_values['orig_private'] = orig.private
          action = 'replace'
      else:
        ns = model.Snippy(keyword=kw, url=url, private=private)
        try:
          ns.put()
        except:
          logging.exception('unable to add new snippy: %s', kw)
          return self.Error('Exception adding new snippy: %s', kw)

        message = 'added! %s -> %s' % (kw, url)
        action = 'update'
        template_values['created'] = kw
      # TODO(ark); send a page showing it created
    else:
      # send a page to edit/create it
      orig = model.GetByKeyword(kw)
      if orig:
        url = orig.url
        alt_url = orig.alt_url
        mobile_url = orig.mobile_url
        suggest_url = orig.suggest_url
        private = orig.private
        action = 'update'
      else:
        message = 'unknown keyword'
        action = 'create'

    template_values['action'] = action
    if kw:
      template_values['keyword'] = kw
    if url:
      template_values['url'] = url
    if alt_url:
      template_values['alt_url'] = alt_url
    if mobile_url:
      template_values['mobile_url'] = mobile_url
    if suggest_url:
      template_values['suggest_url'] = suggest_url
    if private is not None:
      if private:
        template_values['private_yes'] = 'checked'
      else:
        template_values['private_no'] = 'checked'
    if message:
      template_values['message'] = message

    self.SendTemplate('edit.html', template_values)
