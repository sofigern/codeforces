from unittest import TestCase

from dacite import from_dict, Config

from api.submission import Submission, Verdict


class TestSubmissionDataclassSupport(TestCase):
    def test_decode_from_dict_regular(self):
        self.assertEqual(
            from_dict(
                Submission,
                {
                    "id": 1,
                    "contestId": None,
                    "creationTimeSeconds": 100,
                    "relativeTimeSeconds": 200,
                    "problem": {"a": "b"},
                    "author": {"monty": "python"},
                    "programmingLanguage": "python",
                    "verdict": "FAILED",
                    "testset": "TEST",
                    "passedTestCount": 1,
                    "timeConsumedMillis": 42,
                    "memoryConsumedBytes": 100500,
                    "points": 3.14159,
                },
                config=Config(cast=[Verdict])
            ),
            Submission(
                id=1,
                contestId=None,
                creationTimeSeconds=100,
                relativeTimeSeconds=200,
                problem={"a": "b"},
                author={"monty": "python"},
                programmingLanguage="python",
                verdict=Verdict.FAILED,
                testset="TEST",
                passedTestCount=1,
                timeConsumedMillis=42,
                memoryConsumedBytes=100500,
                points=3.14159,
            )
        )
