from dataclasses import dataclass
from typing import Optional, Dict

from codeforces_client.api.verdict import Verdict


@dataclass
class Submission:
    id: int
    contestId: Optional[int]

    # Time, when submission was created, in unix-format.
    creationTimeSeconds: int

    # Number of seconds, passed after the start of the contest
    # (or a virtual start for virtual parties), before the submission.
    relativeTimeSeconds: int

    problem: Dict
    author: Dict
    programmingLanguage: str
    verdict: Optional[Verdict]

    # Enum: SAMPLES, PRETESTS, TESTS, CHALLENGES, TESTS1, ..., TESTS10.
    # Testset used for judging the submission.
    testset: str

    # Number of passed tests.
    passedTestCount: int

    # Maximum time in milliseconds, consumed by solution for one test.
    timeConsumedMillis: int

    # Maximum memory in bytes, consumed by solution for one test.
    memoryConsumedBytes: int

    # Can be absent. Number of scored points for IOI-like contests.
    points: Optional[float]
