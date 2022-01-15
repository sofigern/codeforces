from argparse import Namespace
from itertools import groupby
import os
import shutil

from codeforces_client.api.client import CodeforcesAPIClient
from codeforces_client.api.verdict import Verdict
from codeforces_client.utils.lang2ext import lang2ext


def run(args: Namespace) -> None:
    print("Loading data for")
    for key in ["handle", "contest_id", "verdict", "language"]:
        print(f"\t{key}:", getattr(args, key, "ANY"))

    if args.language.lower() == 'any':
        args.language = None

    os.makedirs(args.handle, exist_ok=True)

    api_client = CodeforcesAPIClient()
    submissions = api_client.user_status(args.handle)
    available_contest_ids = [
        c.id for c in api_client.contest_list()
        if args.contest_id is None or c.id == args.contest_id
    ]

    for (contestId, index), submissions in groupby(
        submissions,
        key=lambda s: (s.contestId, s.problem['index']),
    ):
        if contestId not in available_contest_ids:
            continue
        for (verdict, language), submissions in groupby(
            submissions,
            key=lambda s: (s.verdict, s.programmingLanguage),
        ):
            if args.verdict is not Verdict.ANY and args.verdict is not verdict:
                continue

            if (
                args.language and
                lang2ext(args.language).lower() != lang2ext(language).lower()
            ):
                continue

            latest_submission_id = None

            path = f"{args.handle}/{contestId}/{index}/submissions/{language}/{verdict.value}"

            os.makedirs(path, exist_ok=True)

            for s in submissions:
                submission_path = f"{path}/{s.id}/{s.id}.{lang2ext(language)}"

                if s.id > (latest_submission_id or 0):
                    latest_submission_id = s.id

                if args.force or not os.path.exists(submission_path):
                    os.makedirs(f"{path}/{s.id}", exist_ok=True)
                    code = api_client.scrape_submission_code(s)
                    with open(submission_path, "w") as source_file:
                        source_file.write(code)

            if verdict == Verdict.OK and latest_submission_id:
                shutil.copy(
                    f"{path}/{latest_submission_id}/{latest_submission_id}.{lang2ext(language)}",
                    f"{args.handle}/{contestId}/{index}/{contestId}{index}.{lang2ext(language)}"
                )
