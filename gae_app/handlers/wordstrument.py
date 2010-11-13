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

from lib.sequence import Sequence
import lib.tablature as tablature
from lib.scale import step_patterns

class WordstrumentHandler(webapp.RequestHandler):
  # GET
  def get(self):
    template_values = {
      'http_get': True,
      'scales': step_patterns.keys()
    }

    path = os.path.join(
      os.path.dirname(__file__), '..', 'templates', 'wordstrument.html'
    )
    self.response.out.write(template.render(path, template_values))

  # POST
  def post(self):
    text_in = self.request.get('content')
    scale = self.request.get('scale')

    raw_notes = Sequence(text_in)
    raw_notes_str = raw_notes.to_str()

    raw_notes.setScale(scale)
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
      'vextab_code': tab.to_str()
    }

    path = os.path.join(
      os.path.dirname(__file__), '..', 'templates', 'wordstrument.html'
    )
    self.response.out.write(template.render(path, template_values))
