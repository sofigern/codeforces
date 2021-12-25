import logging
import requests
from typing import List


class CodeforcesAPIClient:
    API_URL = 'https://codeforces.com/api/'

    def __init__(self) -> None:
        logging.info('Starting unauthorised Codeforces API Client.')

    def get_submissions(self, handle: str) -> List[int]:
        pass

