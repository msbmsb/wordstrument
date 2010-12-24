"""
main.py:
Entry point for GAE non-admin.

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'lib'))

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util

import handlers.wordstrument
import handlers.about

def main():
    application = webapp.WSGIApplication([
      ('/', handlers.about.AboutHandler),
      ('/ws', handlers.wordstrument.WordstrumentHandler),
      ('/midi', handlers.wordstrument.MidiHandler),
    ], debug=True)
    util.run_wsgi_app(application)


if __name__ == '__main__':
    main()
