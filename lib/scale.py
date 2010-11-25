"""
scale.py:

Handle all scale-related data and methods.

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

from copy import deepcopy
import globals
from note import Note

_step_patterns = {
  'major':[1,1,0.5,1,1,1,0.5],
  'natural_minor':[1,0.5,1,1,0.5,1,1],
  'harmonic_minor':[1,0.5,1,1,0.5,1.5,0.5],
  'melodic_minor_up':[1,0.5,1,1,1,1,0.5],
  'melodic_minor_down':[1,1,0.5,1,1,0.5,1],
  'dorian':[1,0.5,1,1,1,0.5,1],
  'minor_pentatonic_blues':[1.5,1,1,1.5,1]
}

def get_scale_names():
  return _step_patterns.keys()

def get_default():
  return 'major'

def is_valid_scale(scale_name):
  return scale_name in _step_patterns.keys()

# direction: 1=up, -1=down, None=none-specified
def get_scale(notes, scale, direction=None):
  if scale not in _step_patterns.keys():
    return None

#   if len(notes) < 2:
#     return None

  scale_pattern = _step_patterns[scale]
  
  if not direction or abs(direction) != 1:
    direction = 1

  root = deepcopy(notes[0])

  # move away from min/max octave levels
  if notes[0].octave >= globals.MAX_OCTAVE:
    direction = -1
  if notes[0].octave <= globals.MIN_OCTAVE:
    direction = 1

  allowable_notes = []
  added_notes = []

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

    prev_note = prev.pitch
    prev = deepcopy(new_note)
    new_note.octave = 0
    new_note.duration = 0.0

    # when incrementing up the scale, it is possible to reach a stage where there is:
    # g-n...a-n...a-#...c-n
    # when what is needed is one note instance for all notes in scale, i.e. it's missing the b
    # use alternate notation to turn that a-# into b-flat so that b is represented in scale
    if new_note.pitch in added_notes:
      new_note = new_note.get_alternate_notation()

    allowable_notes.append(new_note)
    added_notes.append(new_note.pitch)

  return allowable_notes
