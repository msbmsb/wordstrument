from math import sqrt
from lib.note import Note
from lib.duration import toVexFlowNotation
import globals

# standard tuning
six_string_std = [
  'e2/n',	'a2/n',	'd3/n',	'g3/n',	'b3/n',	'e4/n',
]

# 27*[6*[""]]
# standard tuning
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
    self.num_frets = 27
    self.num_strings = 6
    self.fret_string_table = []
    if tuning:
      self.buildFretStringTable(tuning)
      self.num_strings = len(tuning)

  def buildFretStringTable(self, tuning):
    self.fret_string_table.append(tuning)
    for f in range(self.num_frets):
      if f == 0: continue
      self.fret_string_table.append([])
      for s in range(len(tuning)):
        prev = Note(self.fret_string_table[f-1][s])
        prev.inc(True)
        self.fret_string_table[f].append(prev.to_str())

  # return the fret-string index of the input note
  # this index is the table index i.e. (0..5), so the string number 
  # is not aligned with typical string numbering i.e. (6..1)
  def index(self, note_in):
    locs = []
    # if is flat, make sharp, the frets are built using only sharps, no flats
    if note_in.accidental == globals.FLAT:
      note_in = note_in.getAlternateNotation()
    note = note_in.to_str()
    for f,fret in enumerate(self.fret_string_table):
      for s,string in enumerate(fret):
        if note.find(self.fret_string_table[f][s]) != -1:
          locs.append((f,s))
    return locs

  # find the nearest fingering on the fretboard for the next note
  # TODO do this in a tripled manner to reduce the number of reverse direction moves
  # i.e. move up two frets for i+1 but i+2 is backward from the ith fret and there is a 2nd-closest
  #      i+1 location that could be used instead. -> minimize movements over groups of notes
  def findNearest(self, current, next_note):
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
    for f,fret in enumerate(self.fret_string_table):
      # fret number
      retVal += "%i\t" % f
      for s,string in enumerate(fret):
        retVal += "%s\t" % self.fret_string_table[f][s]
      retVal += "\n"
    return retVal

class GuitarTabSequence(object):
  def __init__(self, fretboard, note_sequence):
    self.fretboard = fretboard
    self.note_sequence = note_sequence
    self.tab_sequence = []
    self.buildTabSequence()

  def buildTabSequence(self):
    curr = (0,0)
    for n in self.note_sequence.notes:
      if n.note not in globals.PRIMARY_NOTES:
        continue
      nearest = self.fretboard.findNearest(curr, n)
      if not nearest:
        continue
      dur = toVexFlowNotation(n.duration)
      self.tab_sequence.append((nearest,dur))
      curr = self.tab_sequence[-1][0]

  def indexToStringNum(self, index):
    return self.fretboard.num_strings - index

  def to_str(self):
    retVal = ""
    for n in self.tab_sequence:
      retVal += ":%s %i/%i " % (n[-1],n[0][0],self.indexToStringNum(n[0][1]))
    return retVal.strip()
