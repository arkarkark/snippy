# Copyright 2009 Alex K (wtwf.com) All rights reserved.

__author__ = 'wtwf.com (Alex K)'

import logging
import datetime

from wtwf import wtwfhandler
import model

class SearchHandler(wtwfhandler.WtwfHandler):

  @wtwfhandler.admin_required
  def get(self):
    self.post()

  def post(self):
    self.AssertAllowed()

    template_values = {}

    q = self.request.get('q')
    template_values['q'] = q

    query = model.Snippy.query()
    results = []

    checked = self.request.get_all('kw')
    do_update = self.request.get('update')
    do_delete = self.request.get('delete')

    new_priv = self.request.get('private', None)
    if do_update and new_priv is not None:
      new_priv = new_priv == 'yes'

    template_values['update_status'] = do_update or do_delete
    deleted = []

    template_values['message'] = 'no message: %s<br>' % datetime.datetime.now()

    if q:
      template_values['message'] = 'Search results for: %s' % q
      for result in query.fetch(1000):
        if q in result.keyword or q in result.url:
          status = 'No Change'
          if result.keyword in checked:
            if do_update and new_priv is not None:
              if new_priv != result.private:
                result.private = new_priv
                try:
                  result.put()
                  status = 'Updated'
                except:
                  logging.exception('unable to update: %s', result.keyword)
                  status = 'Exception'

            if do_delete:
              deleted.append(result.keyword)
              result.key.delete()
              continue
          toadd = {'keyword': result.keyword,
                   'url': result.url,
                   'private': result.private,
                   'used_count': result.used_count,
                   'checked': result.keyword in checked,
                   'update_status': status
                   }
          if result.keyword == q:
            results.insert(0, toadd)
          else:
            results.append(toadd)
    template_values['results'] = results

    if deleted:
      template_values['message'] = 'Deleted: %s<br />' % ', '.join(deleted)

    self.SendTemplate('search.html', template_values)
