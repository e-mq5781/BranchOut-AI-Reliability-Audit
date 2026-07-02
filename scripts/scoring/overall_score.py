from scripts.scoring.rubric import RUBRIC

def compute_overall(scores): # handle N/A scores
    total = 0
    applicable = 0

    for score, criterion in zip(scores, RUBRIC):
        if score is None:
            continue
        total += score
        applicable += criterion.maximum

    return 100 * total / applicable
