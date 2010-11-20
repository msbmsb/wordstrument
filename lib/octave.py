"""
octave.py

Variables and functions for selecting the octave value for a given string.

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

from math import floor
import unicodedata

_octave_list = [3,3,4,4,4,5,5,5,4,4,4,4,3,3,3,3,2,2,5,5,3,2,2,2,2,2]

def choose_octave(word):
  if(word == None or word == ''):
    return 4

  if type(word) == unicode:
    word = unicodedata.normalize('NFKD', word).encode('ascii','ignore')
  tot = 0
  for c in word.lower():
    n = ord(c) - 97
    if n >= 0 and n < 26:
      tot += n
      
  index = int(floor(tot/len(word)))
  if(index >= 0 and index < 26):
    return _octave_list[index]
  else:
    return 4


