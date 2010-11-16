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
from lib.scale import step_patterns

class WordstrumentHandler(webapp.RequestHandler):
  # GET
  def get(self):
    input = self.request.get('q')
    if input is not None and input != '':
      template_values = self.runWordstrument(
        urllib.unquote_plus(self.request.get('q')), 
        urllib.unquote_plus(self.request.get('s'))
      )
    else:
      template_values = {
        'http_get': True,
        'scales': step_patterns.keys(),
      }

    path = os.path.join(
      os.path.dirname(__file__), '..', 'templates', 'wordstrument.html'
    )
    self.response.out.write(template.render(path, template_values))

  # POST
  def post(self):
    template_values = self.runWordstrument(self.request.get('content'), self.request.get('scale'))

    path = os.path.join(
      os.path.dirname(__file__), '..', 'templates', 'wordstrument.html'
    )
    self.response.out.write(template.render(path, template_values))

  def runWordstrument(self, text_in, scale):
    if text_in is None or text_in == '':
      template_values = {
        'http_get': True,
        'error': "No text to put into the wordstrument. Try again."
      }
      return template_values

    text_in = text_in.strip()
    try:
      raw_notes = Sequence(text_in)
      raw_notes_str = raw_notes.to_str()

      raw_notes.setScale(scale.strip())
      raw_notes.snapToKey()
      in_key_notes_str = raw_notes.to_str()

      # tablature
      fretboard = tablature.GuitarFretboard(tablature.six_string_std)
      tab = tablature.GuitarTabSequence(fretboard, raw_notes)

      template_values = {
        'http_get': False,
        'text_in': text_in,
        'raw_notes': raw_notes_str,
        'root': raw_notes.getRoot(),
        'scale_used': raw_notes.getScaleName(),
        'in_key_notes': in_key_notes_str,
        'scales': step_patterns.keys(),
        'vextab_codes': tab.split_str(),
        'url_query': urllib.urlencode(dict([['q',text_in],['s',raw_notes.getScaleName()]]))
      }
    except DeadlineExceededError:
      template_values = {
        'http_get': True,
        'error': "The request has timed out, please try another."
      }

    return template_values
