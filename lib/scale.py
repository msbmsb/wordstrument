"""
scale.py:

Handle all scale-related data and methods.

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

from copy import deepcopy
import globals
from note import Note

step_patterns = {
  'major':[1,1,0.5,1,1,1,0.5],
  'natural_minor':[1,0.5,1,1,0.5,1,1],
  'harmonic_minor':[1,0.5,1,1,0.5,1.5,0.5],
  'melodic_minor_up':[1,0.5,1,1,1,1,0.5],
  'melodic_minor_down':[1,1,0.5,1,1,0.5,1],
  'dorian':[1,0.5,1,1,1,0.5,1],
  'minor_pentatonic_blues':[1.5,1,1,1.5,1]
}

# direction: 1=up, -1=down, None=none-specified
def get_scale(notes, scale, direction=None):
  if scale not in step_patterns.keys():
    return None

  if len(notes) < 2:
    return None

  scale_pattern = step_patterns[scale]
  
  if not direction or abs(direction) != 1:
    direction = 1

  root = deepcopy(notes[0])

  # move away from min/max octave levels
  if notes[0].octave >= globals.max_octave:
    direction = -1
  if notes[0].octave <= globals.min_octave:
    direction = 1

  allowable_notes = []

  prev = deepcopy(root)
  root.octave = 0
  root.duration = 0.0
  allowable_notes.append(root)
  for p in scale_pattern:
    times = int(p/0.5)
    new_note = prev
    for n in range(times):
      if direction == -1:
        new_note.dec(True)
      else:
        new_note.inc(True)
    # if pitch is same as previous, inc pitch and set accidental
    prev_note = prev.note
    prev = deepcopy(new_note)
    new_note.octave = 0
    new_note.duration = 0.0
    if None and new_note.note == prev_note:
      if direction == -1:
        new_note.decNote()
        new_note.accidental = 'sharp'
      else:
        new_note.incNote()
        new_note.accidental = 'flat'
    allowable_notes.append(new_note)

  print "Allowed: " 
  for a in allowable_notes:
    print "  " + a.to_str()
  return allowable_notes