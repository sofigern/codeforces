from argparse import Namespace
from itertools import groupby
import logging
import os

from codeforces_client.api.client import CodeforcesAPIClient
from codeforces_client.utils.lang2ext import lang2ext


def run(args: Namespace) -> None:
    logging.info("Loading data for handle: %s", args.handle)
    os.makedirs(args.handle, exist_ok=True)

    api_client = CodeforcesAPIClient()
    submissions = api_client.user_status(args.handle)
    available_contest_ids = [c.id for c in api_client.contest_list()]
    for (contestId, index, verdict, language), submissions in groupby(
        submissions,
        key=lambda s: (s.contestId, s.problem['index'], s.verdict, s.programmingLanguage),
    ):
        if contestId not in available_contest_ids:
            continue

        path = f"{args.handle}/{contestId}/{index}/submissions/{language}/{verdict.value}"

        os.makedirs(path, exist_ok=True)
        for s in submissions:
            submision_path = f"{path}/{s.id}/{s.id}.{lang2ext(language)}"

            if args.force or not os.path.exists(submision_path):
                os.makedirs(f"{path}/{s.id}", exist_ok=True)
                code = api_client.scrape_submission_code(s)
                with open(submision_path, "w") as source_file:
                    source_file.write(code)
