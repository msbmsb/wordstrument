"""
accidental.py:

Variables and methods to determine the accidental for a given note.
Natural values are given for all vowels and is used as a tie-breaker,
Sharps and Flats values alternate through the consonants.

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

import random

# from wordstrument
import globals
import selection
from vector_similarity import cosine_similarity

# accidentals variables
sharp = list(globals.alpha)
flat = list(globals.alpha)
natural = list(globals.alpha)

# vowels are natural, natural is the tie-breaker as well
natural[0] = 1.0
natural[4] = 1.0
natural[8] = 1.0
natural[14] = 1.0
natural[20] = 1.0
natural[24] = 1.0

# every other consonant is sharp/flat
sharp[1] = 1.0
sharp[3] = 1.0
sharp[6] = 1.0
sharp[9] = 1.0
sharp[11] = 1.0
sharp[13] = 1.0
sharp[16] = 1.0
sharp[18] = 1.0
sharp[21] = 1.0
sharp[23] = 1.0

flat[2] = 1.0
flat[5] = 1.0
flat[7] = 1.0
flat[10] = 1.0
flat[12] = 1.0
flat[15] = 1.0
flat[17] = 1.0
flat[19] = 1.0
flat[22] = 1.0
flat[25] = 1.0

# given a feature vector and a note, select the accidental
def choose_accidental(fv, note):
  accidental = ''

  scores = {
    'natural':cosine_similarity(natural,fv),
    'sharp':cosine_similarity(sharp,fv),
    'flat':cosine_similarity(flat,fv)
  }
  sorted_scores = sorted(scores.iteritems(), key=lambda (k,v):(v,k), reverse=True)

  if(len(sorted_scores) > 1):
    tops = selection.select_top_same_scores(sorted_scores)
    if('natural' in tops):
      accidental = 'natural'
    else:
      accidental = random.choice(tops)
  else:
    accidental = sorted_scores[0]

  if((accidental == 'flat') and (note == 'c' or note == 'f')):
    accidental = 'natural'
  if((accidental == 'sharp') and (note == 'b' or note == 'e')):
    accidental = 'natural'

  return accidental
