from dataclasses import dataclass
from typing import Optional


@dataclass
class Contest:
    id:	int
    name: str
    type: str  # Enum: CF, IOI, ICPC. Scoring system used for the contest.
    phase: str  # Enum: BEFORE, CODING, PENDING_SYSTEM_TEST, SYSTEM_TEST, FINISHED.

    # If true, then the ranklist for the contest is frozen and shows only submissions,
    # created before freeze.
    frozen: bool
    durationSeconds: int  # Duration of the contest in seconds.
    startTimeSeconds: Optional[int]  # Can be absent. Contest start time in unix format.

    # Number of seconds, passed after the start of the contest. Can be negative.
    relativeTimeSeconds: Optional[int]

    preparedBy: Optional[str]  # Handle of the user, how created the contest.
    websiteUrl: Optional[str]  # URL for contest-related website.
    description: Optional[str]
    difficulty: Optional[int]  # From 1 to 5. Larger number means more difficult problems.

    # Human-readable type of the contest from the following categories: Official ICPC Contest,
    # Official School Contest, Opencup Contest, School/University/City/Region Championship,
    # Training Camp Contest, Official International Personal Contest, Training Contest.
    kind: Optional[str]

    icpcRegion: Optional[str]  # Name of the Region for official ICPC contests.
    country: Optional[str]
    city: Optional[str]
    season: Optional[str]
