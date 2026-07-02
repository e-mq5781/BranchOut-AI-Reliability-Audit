from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class Criterion: # represents one criterion of the rubric, out of like 19
    name: str
    maximum: int # max points possible

RUBRIC = [ # list of criteria
          Criterion("Produced requested output", 7),
          Criterion("Stayed within correct length", 3),
          Criterion("Answered all questions/tasks", 6),
          Criterion("Used requested style", 4),
          Criterion("Factually correct", 18),
          Criterion("No contradictions", 4),
          Criterion("Necessary information", 5),
          Criterion("Grounded claims", 5),
          Criterion("No hallucinated facts", 8),
          Criterion("Logical organization", 4),
          Criterion("Easy to understand", 4),
          Criterion("Appropriate detail", 4),
          Criterion("Appropriate terminology", 3),
          Criterion("Confidence calibration", 4),
          Criterion("Appropriate refusal", 2),
          Criterion("Safe information", 4),
          Criterion("Helpful examples", 3),
          Criterion("Anticipated followups", 3),
          Criterion("Alternatives", 3),
          Criterion("Suggested next steps", 3),
          Criterion("Relevant context", 3),
]

NUM_CRITERIA = len(RUBRIC)

MAX_SCORE = sum(c.maximum for c in RUBRIC)
