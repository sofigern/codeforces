import logging
import requests
from typing import List, Callable
import ujson

import backoff
from dacite import from_dict, Config
from furl import furl
from pyquery import PyQuery


from codeforces_client.api.contest import Contest
from codeforces_client.api.submission import Submission, Verdict


class CodeforcesAPIClient:
    API_URL = "https://codeforces.com/api"

    def __init__(self) -> None:
        logging.info("Starting unauthorised Codeforces API Client.")

    def user_status(self, handle: str) -> List[Submission]:
        logging.debug("Requesting user.status for %s", locals())
        response = requests.get(f"{self.API_URL}/user.status", params={"handle": handle})
        response.raise_for_status()
        result = ujson.loads(response.text)["result"]
        return [
            from_dict(Submission, submission, config=Config(cast=[Verdict]))
            for submission in result
        ]

    def contest_list(self) -> List[Contest]:
        logging.debug("Requesting contest.list")
        response = requests.get(f"{self.API_URL}/contest.list")
        response.raise_for_status()
        result = ujson.loads(response.text)["result"]
        return [from_dict(Contest, contest) for contest in result]

    @staticmethod
    def _make_request(furl: furl) -> requests.Response:
        return requests.get(furl.url)

    def _make_request_safe(self, furl: furl, validator: Callable) -> requests.Response:
        wrap = backoff.on_predicate(
            backoff.expo,
            validator,
            base=60,
            max_value=600,
        )(self._make_request)
        return wrap(furl)

    def scrape_submission_code(self, submission: Submission) -> str:
        logging.debug("Scraping code for %s", submission)
        response = self._make_request_safe(
            furl(
                f"https://codeforces.com/contest/"
                f"{submission.contestId}/submission/{submission.id}"
            ),
            validator=lambda response: not PyQuery(response.text)('#program-source-text')
        )

        return PyQuery(response.text)('#program-source-text').html()
