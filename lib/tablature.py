"""
tablature.py:

Contains two classes:

* GuitarFretboard
  - class for modelling a guitar fretboard given a tuning and number of frets.
* GuitarTabSequence
  - class for generating a tab sequence given a GuitarFretboard and a note Sequence
  - attempts to find the most comfortable/realistic fingering positions for a sequence
  - to_str() outputs in a format intended for vexflow rendering

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

from math import sqrt
from lib.note import Note
from lib.duration import to_vexflow_notation
import globals

# standard tuning
six_string_std = [
  'e2/n',	'a2/n',	'd3/n',	'g3/n',	'b3/n',	'e4/n',
]

# 27*[6*[""]]
# standard tuning
# not actually used since the fretboard is automatically generated
# given the tuning by GuitarFretboard.build_fret_string_table
six_string_fret_notes = [
  ['e2',	'a2',	'd3',	'g3',	'b3',	'e4'],
  ['f2',	'a2#',	'd3#',	'g3#',	'c4',	'f4'],
  ['f2#',	'b2',	'e3',	'a3',	'c4#',	'f4#'],
  ['g2',	'c3',	'f3',	'a3#',	'd4',	'g4'],
  ['g2#',	'c3#',	'f3#',	'b3',	'd4#',	'g4#'],
  ['a2',	'd3',	'g3',	'c4',	'e4',	'a4'],
  ['a2#',	'd3#',	'g3#',	'c4#',	'f4',	'a4#'],
  ['b2',	'e3',	'a3',	'd4',	'f4#',	'b4'],
  ['c3',	'f3',	'a3#',	'd4#',	'g4',	'c5'],
  ['c3#',	'f3#',	'b3',	'e4',	'g4#',	'c5#'],
  ['d3',	'g3',	'c4',	'f4',	'a4',	'd5'],
  ['d3#',	'g3#',	'c4#',	'f4#',	'a4#',	'd5#'],
  ['e3',	'a3',	'd4',	'g4',	'b4',	'e5'],
  ['f3',	'a3#',	'd4#',	'g4#',	'c5',	'f5'],
  ['f3#',	'b3',	'e4',	'a4',	'c5#',	'f5#'],
  ['g3',	'c4',	'f4',	'a4#',	'd5',	'g5'],
  ['g3#',	'c4#',	'f4#',	'b4',	'd5#',	'g5#'],
  ['a3',	'd4',	'g4',	'c5',	'e5',	'a5'],
  ['a3#',	'd4#',	'g4#',	'c5#',	'f5',	'a5#'],
  ['b3',	'e4',	'a4',	'd5',	'f5#',	'b5'],
  ['c4',	'f4',	'a4#',	'd5#',	'g5',	'c6'],
  ['c4#',	'f4#',	'b4',	'e5',	'g5#',	'c6#'],
  ['d4',	'g4',	'c5',	'f5',	'a5',	'd6'],
  ['d4#',	'g4#',	'c5#',	'f5#',	'a5#',	'd6#'],
  ['e4',	'a4',	'd5',	'g5',	'b5',	'e6'],
  ['f4',	'a4#',	'd5#',	'g5#',	'c6',	'f6'],
  ['f4#',	'b4',	'e5',	'a5',	'c6#',	'f6#'],
]

# multiplier to modify the distance from string-to-string over moving to 
# a different fret (i.e. less than 1 makes the distance fn prefer 
# adjacent strings over moving up & down fretboard
STRING_DIST_MUL = 0.5

class GuitarFretboard(object):
  def __init__(self, tuning):
    # default 27 frets
    self.num_frets = 27
    # default 6-string
    self.num_strings = 6
    self._fret_string_table = []
    if tuning:
      self._build_fret_string_table(tuning)
      self.num_strings = len(tuning)

  def _build_fret_string_table(self, tuning):
    self._fret_string_table.append(tuning)
    for f in range(self.num_frets):
      if f == 0: continue
      self._fret_string_table.append([])
      for s in range(len(tuning)):
        prev = Note(self._fret_string_table[f-1][s])
        prev.inc(True)
        self._fret_string_table[f].append(prev.to_str())

  # return the fret-string index of the input note
  # this index is the table index i.e. (0..5), so the string number 
  # is not aligned with typical string numbering i.e. (6..1)
  def index(self, note_in):
    locs = []
    # if is flat, make sharp, the frets are built using only sharps, no flats
    if note_in.accidental == globals.FLAT:
      note_in = note_in.get_alternate_notation()
    note = note_in.to_str()
    for f,fret in enumerate(self._fret_string_table):
      for s,string in enumerate(fret):
        if note.find(self._fret_string_table[f][s]) != -1:
          locs.append((f,s))
    return locs

  # find the nearest fingering on the fretboard for the next note
  # TODO do this in a tripled manner to reduce the number of reverse direction moves
  # i.e. move up two frets for i+1 but i+2 is backward from the ith fret and there is a 2nd-closest
  #      i+1 location that could be used instead. -> minimize movements over groups of notes
  def _find_nearest(self, current, next_note):
    next_locs = self.index(next_note)
    if not next_locs:
      return None
    nearest_loc_index = sorted(dict((i,score) for i,score in enumerate([sqrt((current[0]-loc[0])**2 + ((current[1]-loc[1])*STRING_DIST_MUL)**2) for loc in next_locs])).iteritems(), key=lambda (k,v):(v,k))[0][0]
    return next_locs[nearest_loc_index]

  def to_str(self):
    retVal = "Fretboard-note chart\n"
    retVal += "\t"
    # string numbers
    retVal += '\t'.join([str(i) for i in range(6,0,-1)])
    retVal += '\n'
    for f,fret in enumerate(self._fret_string_table):
      # fret number
      retVal += "%i\t" % f
      for s,string in enumerate(fret):
        retVal += "%s\t" % self._fret_string_table[f][s]
      retVal += "\n"
    return retVal

class GuitarTabSequence(object):
  def __init__(self, fretboard, note_sequence):
    self.fretboard = fretboard
    self.note_sequence = note_sequence
    self._tab_sequence = []
    if note_sequence:
      self._build_tab_sequence()

  def _build_tab_sequence(self):
    curr = (0,0)
    for n in self.note_sequence.notes:
      if n.pitch not in globals.ALL_VALID_NOTES:
        continue
      dur = n.duration
      if n.pitch != globals.REST:
        nearest = self.fretboard._find_nearest(curr, n)
        if not nearest:
          continue
        curr = nearest
      else:
        dur = str(dur) + 'r'
        nearest = (0,0)
      self._tab_sequence.append((nearest,n.text,dur))

  # fret_string: (fret,string)
  def add(self, fret_string, text, dur):
    self._tab_sequence.append((fret_string, text, dur))

  def index_to_string_num(self, index):
    return self.fretboard.num_strings - index

  def split_str(self):
    return self.split_str_by_bars()

  def split_str_by_notes(self, notes_per_split=8):
    start = 0
    end = notes_per_split
    retVal = []
    while start < len(self._tab_sequence):
      retVal.append(self.to_str(start, end-1))
      start += notes_per_split
      end += notes_per_split
    return retVal

  def split_str_by_bars(self, bars_per_split=2):
    if not self.note_sequence.bar_markers:
      return self.split_str_by_notes()

    start = 0
    end_index = bars_per_split-1
    if len(self.note_sequence.bar_markers) > bars_per_split:
      end = self.note_sequence.bar_markers[end_index]
    else:
      end = self.note_sequence.bar_markers[-1]
      end_index = -1
    retVal = []
    while start < len(self._tab_sequence) and start < end:
      retVal.append(self.to_str(start, end))
      start = end + 1
      if end_index >= 0 and \
        len(self.note_sequence.bar_markers) > end_index+bars_per_split:
          end_index += bars_per_split
          end = self.note_sequence.bar_markers[end_index]
      else:
        end = self.note_sequence.bar_markers[-1]
        end_index = -1
    return retVal

  def to_str(self, start=0, end=None):
    retVal = ""
    if end is None or end < start or end > len(self._tab_sequence):
      end = len(self._tab_sequence)
    if start < 0 or start >= end:
      return ""
    i = start
    for n in self._tab_sequence[start:end+1]:
      if i > 0 and i != start and \
        self.note_sequence and (i-1) in self.note_sequence.bar_markers:
          retVal += " | "
      dur = n[-1]
      dvfn = to_vexflow_notation(dur)
      if dvfn is None:
        rest = ''
        if type(dur) is not float and dur[-1] == 'r':
          dur = float(dur[:-1])
          rest = 'r'
        nn0 = dur / 1.5
        nn1 = nn0 * 0.5
        dvfn0 = to_vexflow_notation(str(nn0) + rest)
        dvfn1 = to_vexflow_notation(str(nn1) + rest)
        retVal += self.build_tab_string(n[-2],dvfn0,n[0][0],self.index_to_string_num(n[0][1]))
        retVal += self.build_tab_string(None,dvfn1,n[0][0],self.index_to_string_num(n[0][1]))
      else:
        retVal += self.build_tab_string(n[-2],dvfn,n[0][0],self.index_to_string_num(n[0][1]))
      i += 1
    return retVal.strip()

  def build_tab_string(self, str_, dur, fret, string_):
    retVal = ""
    if str_:
      retVal += "\"%s " % str_
    if dur:
      retVal += ":%s " % dur
    retVal += "%i/%i " % (fret, string_)
    return retVal
