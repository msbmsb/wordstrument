"""
selection.py:

Methods for selecting items from score lists within emitter.py

* Author:       Mitchell Bowden <mitchellbowden AT gmail DOT com>
* License:      MIT License: http://creativecommons.org/licenses/MIT/
"""

def choose_top_score(sorted_scores):
  # if somehow there is no score on anything, return None
  if sorted_scores[0][1] == 0.0:
    return None

  # get the set of same-score tuples at the top and randomly select
  same_score_tuples = select_top_same_scores(sorted_scores)
  return same_score_tuples

# select the tuples with the same highest score
def select_top_same_scores(sorted_scores):
  tss = []
  top = sorted_scores[0][1]
  for t in sorted_scores:
    if t[1] == top:
      tss.append(t[0])
    else:
      break
  return tss
