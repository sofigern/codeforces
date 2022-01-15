from enum import auto

from codeforces_client.utils.auto_name_enum import AutoNameEnum


class Verdict(AutoNameEnum):
    FAILED = auto()
    OK = auto()
    PARTIAL = auto()
    COMPILATION_ERROR = auto()
    RUNTIME_ERROR = auto()
    WRONG_ANSWER = auto()
    PRESENTATION_ERROR = auto()
    TIME_LIMIT_EXCEEDED = auto()
    MEMORY_LIMIT_EXCEEDED = auto()
    IDLENESS_LIMIT_EXCEEDED = auto()
    SECURITY_VIOLATED = auto()
    CRASHED = auto()
    INPUT_PREPARATION_CRASHED = auto()
    CHALLENGED = auto()
    SKIPPED = auto()
    TESTING = auto()
    REJECTED = auto()
    ANY = auto()

    def __str__(self):
        return self.value
