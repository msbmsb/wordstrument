"""
emitter.py:

Main function is emitNote(t). To emit a Note object representing the input string.
Contains helper functions for creating the associated score vector and scoring.

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

from operator import itemgetter
import unicodedata
import re
import random
from string import punctuation

from note import Note
from vector_similarity import cosine_similarity
from vector_similarity import magnitude
from vector_similarity import dot_product
import selection
import octave
import accidental
import duration
import globals

# split on spaces & punctuation
# known abnormality on apostrophes. keep for now.
def string_to_tokens(s):
  return re.sub(r"([\W])", r" \1 ", s.replace('\'','')).split()

# generate a feature vector for a given input word string
def _word_to_fv(word):
  fv = list(globals.ALPHA)

  # normalize all unicode characters
  if type(word) == unicode:
    word = unicodedata.normalize('NFKD', word).encode('ascii','ignore')
  
  for i,c in enumerate(word.lower()):
    n = ord(c) - 97
    if(n < 0):
      n += ord('0')
    if n >= 0 and n < len(fv):
      fv[n] += (1.0 + 0.1*(len(word)-i))/len(word)
      if c in 'abcdefg':
        fv[n] += 0.5/len(word)
  return fv

# based on the input vector, score and return sorted list of notes
# with octave markers
def _score_notes(fv):
  scores = {
    'a3':cosine_similarity(globals.a0,fv),
    'b3':cosine_similarity(globals.b0,fv),
    'c4':cosine_similarity(globals.c0,fv),
    'd4':cosine_similarity(globals.d0,fv),
    'e4':cosine_similarity(globals.e0,fv),
    'f4':cosine_similarity(globals.f0,fv),
    'g4':cosine_similarity(globals.g0,fv),
    'a4':cosine_similarity(globals.a1,fv),
    'b4':cosine_similarity(globals.b1,fv),
    'c5':cosine_similarity(globals.c1,fv),
    'd5':cosine_similarity(globals.d1,fv),
    'e5':cosine_similarity(globals.e1,fv),
    'f5':cosine_similarity(globals.f1,fv),
    'g5':cosine_similarity(globals.g1,fv),
    'a2':cosine_similarity(globals.a2,fv),
    'b2':cosine_similarity(globals.b2,fv),
    'c3':cosine_similarity(globals.c2,fv),
    'd3':cosine_similarity(globals.d2,fv),
    'e3':cosine_similarity(globals.e2,fv),
    'f3':cosine_similarity(globals.f2,fv),
    'g3':cosine_similarity(globals.g2,fv),
    'c2':cosine_similarity(globals.c3,fv),
    'd2':cosine_similarity(globals.d3,fv),
    'e2':cosine_similarity(globals.e3,fv),
    'f2':cosine_similarity(globals.f3,fv),
    'g2':cosine_similarity(globals.g3,fv)
  }
  return sorted(scores.iteritems(), key=lambda (k,v):(v,k), reverse=True)

# based on the input vector, score and return sorted list of notes
# with no octave markers
def _score_notes_no_octave(fv):
  scores = {
    'a':cosine_similarity(globals.a,fv),
    'b':cosine_similarity(globals.b,fv),
    'c':cosine_similarity(globals.c,fv),
    'd':cosine_similarity(globals.d,fv),
    'e':cosine_similarity(globals.e,fv),
    'f':cosine_similarity(globals.f,fv),
    'g':cosine_similarity(globals.g,fv),
  }
  return sorted(scores.iteritems(), key=lambda (k,v):(v,k), reverse=True)

# emit a Note object from the input string
def emit_note(t):
  if t in punctuation:
    return _emit_rest(t)

  fv = _word_to_fv(t)
  sorted_scores = _score_notes_no_octave(fv)

  note = ''
  top_scores = selection.choose_top_score(sorted_scores)
  if(len(top_scores) > 1):
    note = random.choice(top_scores)
  else:
    note = top_scores[0]

  note_to_emit = Note(note+str(octave.choose_octave(t)))
  note_to_emit.accidental = accidental.choose_accidental(fv, note_to_emit.pitch)
  note_to_emit.duration = duration.calculate_duration(t)
  note_to_emit.fv = fv
  note_to_emit.text = t

  return note_to_emit

# emit a rest Note from the input string
def _emit_rest(t):
  note_to_emit = Note(globals.REST_NOTE)
  note_to_emit.text = t
  note_to_emit.duration = None

  # from Michelle
  if(t == ','): note_to_emit.duration = 0.25
  if(t == '.'): note_to_emit.duration = 1.0
  if(t == '?'): note_to_emit.duration = 1.0
  if(t == '!'): note_to_emit.duration = 1.0
  if(t == '-'): note_to_emit.duration = 0.25
  if(t == ':'): note_to_emit.duration = 0.125
  if(t == ';'): note_to_emit.duration = 0.5
  # for joe: TILDEROCK
  if(t == '~'): note_to_emit.duration = 0.03125

  if note_to_emit.duration == None:
    return None

  return note_to_emit

