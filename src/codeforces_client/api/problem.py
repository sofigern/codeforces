from dataclasses import dataclass
from typing import Optional, List


@dataclass
class Problem:
    contestId: Optional[int]  # Id of the contest, containing the problem.
    problemsetName:	Optional[str]  # Short name of the problemset the problem belongs to.

    # Usually, a letter or letter with digit(s) indicating the problem index in a contest.
    index: str
    name: str  # Localized.
    type: str  # Enum: PROGRAMMING, QUESTION.
    points: Optional[float]  # Maximum amount of points for the problem.
    rating: Optional[int]  # Problem rating (difficulty).
    tags: List[str]  # Problem tags.
