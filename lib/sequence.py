from note import Note
import scale
import emitter

class Sequence(object):
  def __init__(self, str):
    self.source_string = str
    self.notes = []
    self.scale_name = ""
    self.scale_notes = []
    self.scale_map = {}
    self.build_notes()

  def build_notes(self):
    toks = emitter.stringToTokens(self.source_string)
    for t in toks:
      n = emitter.emitNote(t)
      self.add(n)

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
      self.getScaleNotes()

  def getRoot(self):
    if self.scale_notes:
      return self.scale_notes[0].note
    elif self.notes:
      return self.notes[0].note
    else:
      return None

  def setScale(self, scale_name):
    if not scale_name: 
      scale_name = 'major'

    if scale_name not in scale.step_patterns:
      # ERROR
      print "ERROR: %s is not a known scale (yet)" % scale_name
      return
    self.scale_name = scale_name
    if len(self.notes) > 0:
      self.getScaleNotes()

  def getScaleName(self):
    return self.scale_name

  def getScaleNotes(self):
    self.scale_notes = scale.get_scale(self.notes, self.scale_name)
    if self.scale_notes:
      for n in self.scale_notes:
        self.scale_map[n.note] = n.accidental

  def snapToKey(self):
    if not self.scale_notes:
      print "ERROR: No scale specified."
      return

    for n in self.notes:
      if n.note == 'P':
        continue
      if n.note not in self.scale_map:
        self.notes.remove(n)
        continue
      n.accidental = self.scale_map[n.note]
