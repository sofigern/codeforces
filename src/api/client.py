import logging
import requests
from typing import List
import ujson

from dacite import from_dict, Config


from api.submission import Submission, Verdict


class CodeforcesAPIClient:
    API_URL = "https://codeforces.com/api"

    def __init__(self) -> None:
        logging.info("Starting unauthorised Codeforces API Client.")

    def user_status(self, handle: str) -> List[Submission]:
        logging.debug("Requesting user.status for %s", locals())
        response = requests.get(f'{self.API_URL}/user.status', params={"handle": handle})
        response.raise_for_status()
        result = ujson.loads(response.text)["result"]
        return [
            from_dict(Submission, submission, config=Config(cast=[Verdict]))
            for submission in result
        ]

