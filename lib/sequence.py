"""
sequence.py:

Contains one class
* Sequence
  - class to represent a Sequence of Notes, given an optional scale specification
  - methods to snap a Sequence of raw Notes to a given scale to keep it in key

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

from copy import deepcopy

from note import Note
import scale
import emitter
import globals

class Sequence(object):
  def __init__(self, str_):
    self.source_string = str_.strip()
    self.notes = []
    self.scale_name = ""
    self.scale_notes = []
    self.scale_map = {}
    if str_:
      self.build_notes()
    self.beats_per_bar = 1.0
    # index of bar_markers is the end of a bar
    self.bar_markers = []

  def build_notes(self):
    toks = emitter.string_to_tokens(self.source_string)
    prev = None
    for t in toks:
      n = emitter.emit_note(t)
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
        if n.pitch != globals.REST:
          prev = n

  def to_str(self):
    retStr = ""
    if not self.notes:
      return retStr

    for i,n in enumerate(self.notes):
      retStr += "| %s " % n.to_str()
      if i in self.bar_markers:
        retStr += " BAR| "
    return retStr

  def add(self, note):
    self.notes.append(note)
    if not self.scale_notes and \
        self.notes and len(self.notes) > 0 and \
        len(self.scale_name) > 0:
      self.set_scale_map()

  def get_root(self):
    if self.scale_notes:
      return self.scale_notes[0].pitch
    elif self.notes:
      return self.notes[0].pitch
    else:
      return None

  def fill_sequence(self, starting_from, ending_at):
    if not self.scale_name:
      self.setScale(None)
    curr = starting_from
    done = False
    while not done:
      if self.check_scale(curr):
        self.add(deepcopy(curr))
      else:
        alt = curr.get_alternate_notation()
        if self.check_scale(alt):
          self.add(deepcopy(alt))
          curr = alt
      curr.inc(True)
      if curr.is_equiv_to(ending_at):
        done = True

  def check_scale(self, note):
    n_acc = self.scale_map[note.pitch]
    if note.accidental != n_acc:
      return False
    else:
      return True

  def set_scale(self, scale_name):
    if not scale_name: 
      scale_name = scale.get_default()

    if not scale.is_valid_scale(scale_name):
      # ERROR
      print "ERROR: %s is not a known scale (yet)" % scale_name
      return
    self.scale_name = scale_name
    if len(self.notes) > 0:
      self.set_scale_map()

  def get_scale_name(self):
    return self.scale_name

  def get_scale_map(self):
    return self.scale_map

  def set_scale_map(self):
    self.scale_notes = scale.get_scale(self.notes, self.scale_name)
    if self.scale_notes:
      for n in self.scale_notes:
        self.scale_map[n.pitch] = n.accidental

  def snap_to_key(self):
    if not self.scale_notes:
      print "ERROR: No scale specified."
      return

    for n in self.notes:
      if n.pitch == globals.REST:
        continue
      if n.pitch not in self.scale_map:
        self.notes.remove(n)
        continue

      n.accidental = self.scale_map[n.pitch]

  # modify durations as necessary to fit notes into time signature
  # specified by self.beats_per_bar
  def snap_to_time_signature(self):
    if not self.beats_per_bar or self.beats_per_bar <= 0.1:
      print "ERROR: No time signature specified."
      return

    bar_duration = 0.0
    for i,n in enumerate(self.notes):
      if not n.duration:
        continue
      nextsum = bar_duration + n.duration
      if nextsum > self.beats_per_bar:
        # modify last note's duration to fit
        # set bar marker to this index
        diff = self.beats_per_bar - bar_duration
        if diff not in globals.VALID_DURATIONS and \
          globals.VALID_DURATIONS[0] < diff and \
          globals.VALID_DURATIONS[-1] > diff:
          # find the next smallest duration to diff
          # VALID_DURATIONS is short and sorted, just linearly iterate
          for j in range(len(globals.VALID_DURATIONS[1:])):
            if globals.VALID_DURATIONS[j] > diff:
              if globals.VALID_DURATIONS[j-1] == n.duration and j > 1:
                n.duration = globals.VALID_DURATIONS[j-2]
              else:
                n.duration = globals.VALID_DURATIONS[j-1]
              break
        else:
          n.duration = diff
        nextsum = bar_duration + n.duration

      if nextsum == self.beats_per_bar:
        bar_duration = 0.0
        self.bar_markers.append(i)
      else:
        if i == len(self.notes)-1:
          diff = self.beats_per_bar - bar_duration
          n.duration = diff
          self.bar_markers.append(i)
        else:
          bar_duration = nextsum
