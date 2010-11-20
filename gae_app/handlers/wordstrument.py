"""
wordstrument.py:

Handler for Wordstrument

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

import os
import traceback
import time
import yaml
import logging
import urllib

from lib.sequence import Sequence
import lib.tablature as tablature
from lib.scale import get_scale_names

class WordstrumentHandler(webapp.RequestHandler):
  # GET
  def get(self):
    input = self.request.get('q')
    if input is not None and input != '':
      template_values = self.run_wordstrument(
        urllib.unquote_plus(self.request.get('q')), 
        urllib.unquote_plus(self.request.get('s'))
      )
    else:
      template_values = {
        'http_get': True,
        'scales': get_scale_names(),
      }

    path = os.path.join(
      os.path.dirname(__file__), '..', 'templates', 'wordstrument.html'
    )
    self.response.out.write(template.render(path, template_values))

  # POST
  def post(self):
    template_values = self.run_wordstrument(self.request.get('content'), self.request.get('scale'))

    path = os.path.join(
      os.path.dirname(__file__), '..', 'templates', 'wordstrument.html'
    )
    self.response.out.write(template.render(path, template_values))

  def run_wordstrument(self, text_in, scale):
    if text_in is None or text_in == '':
      template_values = {
        'http_get': True,
        'error': "No text to put into the wordstrument. Try again."
      }
      return template_values

    text_in = text_in.strip()
    raw_notes = Sequence(text_in)
    raw_notes_str = raw_notes.to_str()

    raw_notes.set_scale(scale.strip())
    raw_notes.snap_to_key()
    raw_notes.snap_to_time_signature()
    in_key_notes_str = raw_notes.to_str()

    # tablature
    fretboard = tablature.GuitarFretboard(tablature.six_string_std)
    tab = tablature.GuitarTabSequence(fretboard, raw_notes)

    template_values = {
      'http_get': False,
      'text_in': text_in,
      'raw_notes': raw_notes_str,
      'root': raw_notes.get_root(),
      'scale_used': raw_notes.get_scale_name(),
      'in_key_notes': in_key_notes_str,
      'scales': get_scale_names(),
      'vextab_codes': tab.split_str(),
      'url_query': urllib.urlencode(dict([['q',text_in],['s',raw_notes.get_scale_name()]]))
    }

    return template_values
