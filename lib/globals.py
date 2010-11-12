"""
globals.py:

Global variable values for use in wordstrument. Contains the mappings for 
characters to notes.

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

# globals
primary_notes = 'abcdefg'
allalpha = 'abcdefghijklmnopqrstuvwxyz'
alpha = 26*[0.0]

# with octaves
a0 = list(alpha)
b0 = list(alpha)
c0 = list(alpha)
d0 = list(alpha)
e0 = list(alpha)
f0 = list(alpha)
g0 = list(alpha)
a1 = list(alpha)
b1 = list(alpha)
c1 = list(alpha)
d1 = list(alpha)
e1 = list(alpha)
f1 = list(alpha)
g1 = list(alpha)
a2 = list(alpha)
b2 = list(alpha)
c2 = list(alpha)
d2 = list(alpha)
e2 = list(alpha)
f2 = list(alpha)
g2 = list(alpha)
c3 = list(alpha)
d3 = list(alpha)
e3 = list(alpha)
f3 = list(alpha)
g3 = list(alpha)

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
a = list(alpha)
b = list(alpha)
c = list(alpha)
d = list(alpha)
e = list(alpha)
f = list(alpha)
g = list(alpha)

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

max_octave = 6
min_octave = 2
