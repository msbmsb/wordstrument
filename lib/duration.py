"""
duration.py:

Given a string, calculate the duration of the corresponding note.
The average English word is roughly 5 characters long, based on that:

# of characters     note duration
0-1                 1/16th
2-3                 1/8th
4-6                 1/4
7-8                 1/2
9-10                1
11+                 2

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

# given a string, calculate the duration of the corresponding note
def calculate_duration(t):
  # avg English word len is ~5
  l = len(t)
  if(l<2): return 0.0625
  if(l<4): return 0.125
  if(l<7): return 0.25
  if(l<9): return 0.5
  if(l<11): return 1
  return 2

