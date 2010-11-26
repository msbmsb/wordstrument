"""
note.py:

Contains one class
* Note
  - class to represent a note including pitch, duration, accidental, associated text
  - methods to increment and decrement a Note
  - comparison, equivalence and difference methods
  - method to get alternate notation writings (e.g. A#/Bb)

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

from copy import deepcopy
import globals

class Note(object):
  def __init__(self, note_in):
    note = deepcopy(note_in)
    self.pitch = note[0]
    if len(note) > 1:
      self.octave = int(note[1])
    else:
      self.octave = 4
    if len(note) > 2:
      self.accidental = note[-1]
    else:
      self.accidental = globals.NATURAL
    self.duration = None
    self.fv = []
    self.text = None

  def to_str(self):
    if self.duration:
      return "%s%s/%s/%s" % (self.pitch, self.octave, self.accidental, self.duration)
    else:
      return "%s%s/%s" % (self.pitch, self.octave, self.accidental)

  def to_str_normal(self):
    return "%s%s%s" % (self.pitch.upper(), self.octave, self.accidental)

  def pitch_to_index(self, note_in=None):
    whatToIndex = self.pitch
    if note_in:
      whatToIndex = note_in
    
    if whatToIndex not in globals.PRIMARY_NOTES:
      return None

    return globals.PRIMARY_NOTES.index(whatToIndex)

  def index_to_note(self, index):
    if index > 6 or index < 0:
      return None

    return globals.PRIMARY_NOTES[index]

  def is_identical_to(self, other, noOctave=None):
    # check for surface identity
    if (self.pitch == other.pitch) and \
       (self.accidental == other.accidental):
      if noOctave:
        return True
      if self.octave == other.octave:
        return True
      else:
        return False

  # is self equivalent to other
  # check for identity and
  # include comparisons for enharmonics
  def is_equiv_to(self, other, noOctave=None):
    if self.is_identical_to(other, noOctave):
      return True

    # if both are natural, or both have same accidental,
    # then it cannot be equivalent through sharp/flat
    if (self.accidental == globals.NATURAL and other.accidental == globals.NATURAL) or \
       (self.accidental == other.accidental):
      return False

    # find the sharp
    sharp_note = None
    other_note = None
    if self.accidental == globals.SHARP:
      sharp_note = self
      other_note = other
    elif other.accidental == globals.SHARP:
      sharp_note = other
      other_note = self 
    if sharp_note:
      # drop accidental, increment 1, decrement by 0.5 and compare
      sharp_note.accidental = globals.NATURAL
      sharp_note.inc()
      sharp_note.dec(True)
      if not sharp_note.is_identical_to(other_note, noOctave):
        return False
    # if dne, find the flat
    else:
      flat_note = None
      if self.accidental == globals.FLAT:
        flat_note = self
        other_note = other
      elif other.accidental == globals.FLAT:
        flat_note = other
        other_note = self 
      if flat_note:
        # drop accidental, decrement 1, increment by 0.5 and compare
        flat_note.accidental = globals.NATURAL
        flat_note.dec()
        flat_note.inc(True)
        if not flat_note.is_identical_to(other_note, noOctave):
          return False
      else:
        return False

    # cannot be more than one octave level away
    # e.g {a4-flat, g3-sharp} are equivalent
    if not noOctave and abs(self.octave - other.octave) > 1:
      return False

    # cannot be more than one pitch away
    # e.g. {a4-sharp, b4-flat} are equivalent
    #      {a4-sharp, c4} are not
    if abs(self.pitch_to_index() - other.pitch_to_index()) > 1:
      return False
    

  # compare self against other
  #   thisnote.compare(other)
  # return 1 for greater than, -1 for less than, 0 for equal
  # default parameter noOctave specifies whether to compare 
  # disregarding the octave (i.e. only a-g) or not
  def compare(self, other, noOctave=None):
    if other == None:
      return None

    if self.pitch == globals.REST or other.pitch == globals.REST:
      return None

    if noOctave:
      return self.compare_no_octave(other)

    if self.is_equiv_to(other):
      return 0

    # absolute compare, including octave
    if self.octave > other.octave:
      return 1
    if other.octave > self.octave:
      return -1

    # else, notes are in the same octave, different notes
    return self.compare_no_octave(other)

  # compare notes on a [0..6] range
  # disregarding the octave (i.e. only a-g)
  # return 1 for greater than, -1 for less than, 0 for equal
  def compare_no_octave(self, other):
    if other == None:
      return None

    if self.is_equiv_to(other, True):
      return 0
    if self.pitch_to_index() > other.pitch_to_index():
      return 1
    if other.pitch_to_index() > self.pitch_to_index():
      return -1
    if self.accidental == globals.SHARP and other.accidental != globals.SHARP:
      return 1
    if other.accidental == globals.SHARP and self.accidental != globals.SHARP:
      return -1
    return 0

  def difference(self, other_in):
    comp = self.compare(other_in)
    if comp is None:
      return None
    if comp == 0:
      return 0

    # self > other
    other = deepcopy(other_in)
    diff = 0
    if comp == 1:
      while not other.compare(self) == 0:
        other.inc(True)
        diff += 0.5
    if comp == -1:
      while not other.compare(self) == 0:
        other.dec(True)
        diff -= 0.5
    return diff

  # get the alternate writing of this note, if exists
  # e.g. a# == b-flat
  def get_alternate_notation(self):
    new_note = deepcopy(self)

    # if c or f, the only alternate is b# or e#
    if new_note.accidental == globals.NATURAL and \
        (new_note.pitch == 'f' or new_note.pitch == 'c'):
      new_note.dec()
      new_note.accidental = globals.SHARP
      return new_note

    # if note is sharp, return next pitch, flat
    if new_note.accidental == globals.SHARP:
      new_note.inc()
      new_note.accidental = globals.FLAT
      return new_note

    # if note is flat, return prev pitch, sharp
    if new_note.accidental == globals.FLAT:
      new_note.dec()
      new_note.accidental = globals.SHARP
      return new_note

    # otherwise, if note is not c/f and is natural, there is no alternate
    return self

  # increment
  def inc(self, half=None):
    if half:
      # if note is flat, make it natural and return
      if self.accidental == globals.FLAT:
        self.accidental = globals.NATURAL
        return

      # if note not sharp and can be sharp, make it sharp
      # otherwise increment note
      if self.accidental != globals.SHARP:
        if self.pitch != 'b' and self.pitch != 'e':
          self.accidental = globals.SHARP
          return
        else:
          # b or e
          return self._inc_note()
      else:
        # if already sharp, make it natural and increment note
        self.accidental = globals.NATURAL
        return self._inc_note()

    else:
      # whole increment
      self._inc_note()
      if self.pitch == 'c' or self.pitch == 'f':
        self.accidental = globals.SHARP

  def _inc_note(self):
    index = self.pitch_to_index()
    if index == None:
      return
    index += 1
    index = index % 7
    if index == 0:
      self.octave += 1
    self.pitch = self.index_to_note(index)
    self.adjust_accidental()

  # decrement
  def dec(self, half=None):
    if half:
      # if note is sharp, make it natural and return
      if self.accidental == globals.SHARP:
        self.accidental = globals.NATURAL
        return

      # if note not flat and can be flat, make it flat
      # otherwise increment note
      if self.accidental != globals.FLAT:
        if self.pitch != 'c' and self.pitch != 'f':
          self.accidental = globals.FLAT
          return
        else:
          # c or f
          return self._dec_note()
      else:
        # if already flat, make it natural and decrement note
        self.accidental = globals.NATURAL
        return self._dec_note()

    else:
      # whole decrement
      self._dec_note()
      if self.pitch == 'b' or self.pitch == 'e':
        self.accidental = globals.FLAT

  def _dec_note(self):
    index = self.pitch_to_index()
    if index == None:
      return
    index -= 1
    index = index % 7
    if index == 6:
      self.octave -= 1
    self.pitch = self.index_to_note(index)
    self.adjust_accidental()

  def adjust_accidental(self):
    if self.pitch in ['b','e'] and self.accidental == globals.SHARP:
      self.accidental = globals.NATURAL
    if self.pitch in ['c','f'] and self.accidental == globals.FLAT:
      self.accidental = globals.NATURAL
