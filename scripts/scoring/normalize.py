from typing import Iterable

from scripts.scoring.rubric import MAX_SCORE


# all normalizing functions to normalize the score
def normalize(score, maximum):
    return score / maximum

def normalize_vector(scores, maximums):
    return [ s / m for s,m in zip(scores, maximums) ]

def renormalize(total, applicable):
    if applicable == 0:
        return 0.0

    return 100.0 * total / applicable
