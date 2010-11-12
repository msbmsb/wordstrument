from globals import primary_notes

class Note(object):
  def __init__(self, note):
    self.note = note[0]
    self.octave = int(note[1])
    self.accidental = None
    self.duration = None
    self.fv = []

  def to_str(self):
    return "%s%s/%s/%s" % (self.note, self.octave, self.accidental, self.duration)

  def noteToIndex(self, note_in=None):
    whatToIndex = self.note
    if note_in:
      whatToIndex = note_in
    
    if whatToIndex not in primary_notes:
      return None

    return primary_notes.index(whatToIndex)

  def indexToNote(self, index):
    if index > 6 or index < 0:
      return None

    return primary_notes[index]

  def is_identical_to(self, other, noOctave=None):
    # check for surface identity
    if (self.note == other.note) and \
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
    if (self.accidental == 'natural' and other.accidental == 'natural') or \
       (self.accidental == other.accidental):
      return False

    # find the sharp
    sharp_note = None
    other_note = None
    if self.accidental == 'sharp':
      sharp_note = self
      other_note = other
    elif other.accidental == 'sharp':
      sharp_note = other
      other_note = self 
    if sharp_note:
      # drop accidental, increment 1, decrement by 0.5 and compare
      sharp_note.accidental = 'natural'
      sharp_note.inc()
      sharp_note.dec(True)
      if not sharp_note.is_identical_to(other_note, noOctave):
        return False
    # if dne, find the flat
    else:
      flat_note = None
      if self.accidental == 'flat':
        flat_note = self
        other_note = other
      elif other.accidental == 'flat':
        flat_note = other
        other_note = self 
      if flat_note:
        # drop accidental, decrement 1, increment by 0.5 and compare
        flat_note.accidental = 'natural'
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
    if abs(self.noteToIndex() - other.noteToIndex()) > 1:
      return False
    

  # compare self against other
  #   thisnote.compare(other)
  # return 1 for greater than, -1 for less than, 0 for equal
  # default parameter noOctave specifies whether to compare 
  # disregarding the octave (i.e. only a-g) or not
  def compare(self, other, noOctave=None):
    if other == None:
      return None

    if noOctave:
      return self.compareNoOctave(other)

    if self.is_equiv_to(other):
      return 0

    # absolute compare, including octave
    if self.octave > other.octave:
      return 1
    if other.octave > self.octave:
      return -1

    # else, notes are in the same octave, different notes
    return self.compareNoOctave(other)

  # compare notes on a [0..6] range
  # disregarding the octave (i.e. only a-g)
  # return 1 for greater than, -1 for less than, 0 for equal
  def compareNoOctave(self, other):
    if other == None:
      return None

    if self.is_equiv_to(other, True):
      return 0
    if self.note > other.note:
      return 1
    if other.note > self.note:
      return -1
    if self.accidental == 'sharp' and other.accidental != 'sharp':
      return 1
    if other.accidental == 'sharp' and self.accidental != 'sharp':
      return -1
    return 0

  def difference(self, other):
    comp = self.compare(other)
    if comp == 0:
      return 0

    # self > other
    diff = 0
    if comp == 1:
      while not other.compare(self) == 0:
        other.inc(True)
        diff += 0.5
    if comp == -11:
      while not other.compare(self) == 0:
        other.dec(True)
        diff -= 0.5
    return diff


  # increment
  def inc(self, half=None):
    if half:
      # if note is flat, make it natural and return
      if self.accidental == 'flat':
        self.accidental = 'natural'
        return

      # if note not sharp and can be sharp, make it sharp
      # otherwise increment note
      if self.accidental != 'sharp':
        if self.note != 'b' and self.note != 'e':
          self.accidental = 'sharp'
          return
        else:
          # b or e
          return self.incNote()
      else:
        # if already sharp, make it natural and increment note
        self.accidental = 'natural'
        return self.incNote()

    else:
      # whole increment
      self.incNote()
      if self.note == 'c' or self.note == 'f':
        self.accidental = 'sharp'

  def incNote(self):
    index = self.noteToIndex()
    if index == None:
      return
    index += 1
    index = index % 7
    if index == 0:
      self.octave += 1
    self.note = self.indexToNote(index)
    self.adjustAccidental()

  # decrement
  def dec(self, half=None):
    if half:
      # if note is sharp, make it natural and return
      if self.accidental == 'sharp':
        self.accidental = 'natural'
        return

      # if note not flat and can be flat, make it flat
      # otherwise increment note
      if self.accidental != 'flat':
        if self.note != 'c' and self.note != 'f':
          self.accidental = 'flat'
          return
        else:
          # c or f
          return self.decNote()
      else:
        # if already flat, make it natural and decrement note
        self.accidental = 'natural'
        return self.decNote()

    else:
      # whole decrement
      self.decNote()
      if self.note == 'b' or self.note == 'e':
        self.accidental = 'flat'

  def decNote(self):
    index = self.noteToIndex()
    if index == None:
      return
    index -= 1
    index = index % 7
    if index == 6:
      self.octave -= 1
    self.note = self.indexToNote(index)
    self.adjustAccidental()

  # TODO: c-flat is a b, b-sharp is a c, etc.
  def adjustAccidental(self):
    if self.note in ['b','e'] and self.accidental == 'sharp':
      self.accidental = 'natural'
    if self.note in ['c','f'] and self.accidental == 'flat':
      self.accidental = 'natural'
