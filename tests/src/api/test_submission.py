from unittest import TestCase

from dacite import from_dict, Config

from codeforces_client.api.submission import Submission, Verdict, Problem


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
                    "problem": {
                        "contestId": None,
                        "problemsetName": "problemsetname",
                        "index": "A1",
                        "name": "Ветчина",
                        "type": "PROGRAMMING",
                        "points": 3.14,
                        "rating": 1000,
                        "tags": ["spam", "egg"],
                    },
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
                problem=Problem(
                    contestId=None,
                    problemsetName="problemsetname",
                    index="A1",
                    name="Ветчина",
                    type="PROGRAMMING",
                    points=3.14,
                    rating=1000,
                    tags=["spam", "egg"],
                ),
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
