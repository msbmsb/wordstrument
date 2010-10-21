"""
vector_similarity.py:
Functions for calculating IR-style vector similarity

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

from itertools import imap
from math import sqrt
from operator import mul

def dot_product(vector1, vector2):
  return sum(imap(mul, vector1, vector2))

def magnitude(vector):
  return sqrt(sum(imap(mul, vector, vector)))

def cosine_similarity(vector1, vector2):
  return dot_product(vector1, vector2)/(magnitude(vector1) * magnitude(vector2))
