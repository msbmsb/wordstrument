"""
sequence.py:

Contains one class
* Sequence
  - class to represent a Sequence of Notes, given an optional scale specification
  - methods to snap a Sequence of raw Notes to a given scale to keep it in key

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

from note import Note
import scale
import emitter
import globals

class Sequence(object):
  def __init__(self, str):
    self.source_string = str.strip()
    self.notes = []
    self.scale_name = ""
    self.scale_notes = []
    self.scale_map = {}
    self.build_notes()
    self.beats_per_bar = 1.0

  def build_notes(self):
    toks = emitter.stringToTokens(self.source_string)
    prev = None
    for t in toks:
      n = emitter.emitNote(t)
      if n is not None:
        if prev:
          # check difference of new note to previous one
          # avoid wild swings up & down the octaves
          diff = n.difference(prev)
          if diff is not None and abs(diff) >= 6.0:
            octmod = abs(int(diff/6.0))
            if diff > 0:
              n.octave -= octmod
            elif diff < 0:
              n.octave += octmod
        self.add(n)
        if n.note != globals.REST:
          prev = n

  def to_str(self):
    retStr = ""
    if not self.notes:
      return retStr

    for n in self.notes:
      retStr += "| %s " % n.to_str()
    return retStr

  def add(self, note):
    self.notes.append(note)
    if not self.scale_notes and \
        self.notes and len(self.notes) > 0 and \
        len(self.scale_name) > 0:
      self.setScaleMap()

  def getRoot(self):
    if self.scale_notes:
      return self.scale_notes[0].note
    elif self.notes:
      return self.notes[0].note
    else:
      return None

  def setScale(self, scale_name):
    if not scale_name: 
      scale_name = scale.step_patterns.keys()[0]

    if scale_name not in scale.step_patterns.keys():
      # ERROR
      print "ERROR: %s is not a known scale (yet)" % scale_name
      return
    self.scale_name = scale_name
    if len(self.notes) > 0:
      self.setScaleMap()

  def getScaleName(self):
    return self.scale_name

  def getScaleMap(self):
    return self.scale_map

  def setScaleMap(self):
    self.scale_notes = scale.get_scale(self.notes, self.scale_name)
    if self.scale_notes:
      for n in self.scale_notes:
        self.scale_map[n.note] = n.accidental

  def snapToKey(self):
    if not self.scale_notes:
      print "ERROR: No scale specified."
      return

    for n in self.notes:
      if n.note == globals.REST:
        continue
      if n.note not in self.scale_map:
        self.notes.remove(n)
        continue

      n.accidental = self.scale_map[n.note]
