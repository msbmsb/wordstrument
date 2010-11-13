"""
globals.py:

Global variable values for use in wordstrument. Contains the mappings for 
characters to notes.

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

# globals
PRIMARY_NOTES = 'cdefgab'
PAUSE = 'P0'
ALLALPHA = 'abcdefghijklmnopqrstuvwxyz'
ALPHA = 26*[0.0]

# with octaves
a0 = list(ALPHA)
b0 = list(ALPHA)
c0 = list(ALPHA)
d0 = list(ALPHA)
e0 = list(ALPHA)
f0 = list(ALPHA)
g0 = list(ALPHA)
a1 = list(ALPHA)
b1 = list(ALPHA)
c1 = list(ALPHA)
d1 = list(ALPHA)
e1 = list(ALPHA)
f1 = list(ALPHA)
g1 = list(ALPHA)
a2 = list(ALPHA)
b2 = list(ALPHA)
c2 = list(ALPHA)
d2 = list(ALPHA)
e2 = list(ALPHA)
f2 = list(ALPHA)
g2 = list(ALPHA)
c3 = list(ALPHA)
d3 = list(ALPHA)
e3 = list(ALPHA)
f3 = list(ALPHA)
g3 = list(ALPHA)

a0[0] = 1.0 #a -> a3
b0[1] = 1.0 #b -> b3
c0[2] = 1.0 #c -> c4
d0[3] = 1.0 #d -> d4
e0[4] = 1.0 #e -> e4
f0[5] = 1.0 #f -> f4
g0[6] = 1.0 #g -> g4
g1[7] = 1.0 #h -> a4
f1[8] = 1.0 #i -> b4
e1[9] = 1.0 #j -> c5
d1[10] = 1.0 #k -> d5
c1[11] = 1.0 #l -> e5
b1[12] = 1.0 #m -> f5
a1[13] = 1.0 #n -> g5
a2[14] = 1.0 #o -> a2
b2[15] = 1.0 #p -> b2
c2[16] = 1.0 #q -> c3
d2[17] = 1.0 #r -> d3
e2[18] = 1.0 #s -> e3
f2[19] = 1.0 #t -> f3
g2[20] = 1.0 #u -> g3
g3[21] = 1.0 #v -> c2
f3[22] = 1.0 #w -> d2
e3[23] = 1.0 #x -> e2
d3[24] = 1.0 #y -> f2
c3[25] = 1.0 #z -> g2

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
