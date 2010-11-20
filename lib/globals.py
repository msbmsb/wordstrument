"""
globals.py:

Global variable values for use in wordstrument. Contains the mappings for 
characters to notes, allowable characters and so on.

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

# globals
PRIMARY_NOTES = 'cdefgab'
REST = 'R'
ALL_VALID_NOTES = PRIMARY_NOTES + REST
REST_NOTE = 'R0'
ALLALPHA = 'abcdefghijklmnopqrstuvwxyz'
ALPHA = 26*[0.0]

# no octaves
a = list(ALPHA)
b = list(ALPHA)
c = list(ALPHA)
d = list(ALPHA)
e = list(ALPHA)
f = list(ALPHA)
g = list(ALPHA)

a[0] = 1.0
a[13] = 1.0
a[14] = 1.0
b[1] = 1.0
b[12] = 1.0
b[15] = 1.0
c[2] = 1.0
c[11] = 1.0
c[16] = 1.0
c[25] = 1.0
d[3] = 1.0
d[10] = 1.0
d[17] = 1.0
d[24] = 1.0
e[4] = 1.0
e[9] = 1.0
e[18] = 1.0
e[23] = 1.0
f[5] = 1.0
f[8] = 1.0
f[19] = 1.0
f[22] = 1.0
g[6] = 1.0
g[7] = 1.0
g[20] = 1.0
g[21] = 1.0

MAX_OCTAVE = 6
MIN_OCTAVE = 2

SHARP = '#'
FLAT = 'b'
NATURAL = 'n'

VALID_DURATIONS = [
  0.03125,
  0.0625,
  0.125,
  0.25,
  0.375,
  0.5,
  0.75,
  1.0
]
