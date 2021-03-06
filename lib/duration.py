"""
duration.py:

Given a string, calculate the duration of the corresponding note.
The average English word is roughly 5 characters long, based on that:

# of characters     note duration
0-1                 1/32
2                   1/16
3-4                 1/8
5-8                 1/4
9-10                1/2
11+                 1

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

# given a string, calculate the duration of the corresponding note
def calculate_duration(t):
  # avg English word len is ~5
  l = len(t)
  if(l<2): return 0.03125 # 1
  if(l<3): return 0.0625 # 2
  if(l<5): return 0.125 # 3-4
  if(l<9): return 0.25 # 5-8
  if(l<11): return 0.5 # 9-10
  return 1.0 # 11+

# VexFlow notation
_vexflow_notation = {
  0.03125:'32',
  0.0625:'16',
  0.125:'8',
  0.25:'q',
  0.375:'qd',
  0.5:'h',
  0.75:'hd',
  1.0:'w'
}

# vexflow does not currently output qdr, hdr
_no_matching_vexflow_notation = [
  '0.75r', '0.375r'
]

_vexflow_to_normal_notation = dict(
  (v,k) for k, v in _vexflow_notation.iteritems()
)

# transform float duration to vexflow notation
def to_vexflow_notation(d):
  if not d:
    # default
    return 'q'

  if d in _no_matching_vexflow_notation:
    return None

  rest = ''
  if type(d) is not float and d[-1] == 'r':
    k = float(d[:-1])
    rest = 'r'
  else:
    k = d
    if k not in _vexflow_notation.keys():
      return None
  return str(_vexflow_notation[k]) + rest
