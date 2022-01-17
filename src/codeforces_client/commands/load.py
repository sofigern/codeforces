import logging
from argparse import Namespace
from itertools import groupby
import os
import shutil

from codeforces_client.api.client import CodeforcesAPIClient
from codeforces_client.api.submission import Submission
from codeforces_client.api.verdict import Verdict
from codeforces_client.utils.lang2ext import lang2ext


def download_submission(
        api_client: CodeforcesAPIClient,
        s: Submission,
        path: str,
        rewrite: bool = False,
) -> None:
    submission_path = f"{path}/{s.id}/{s.id}.{lang2ext(s.programmingLanguage)}"
    if rewrite or not os.path.exists(submission_path):
        os.makedirs(f"{path}/{s.id}", exist_ok=True)
        code = api_client.scrape_submission_code(s)
        with open(submission_path, "w") as source_file:
            source_file.write(code)


def run(args: Namespace) -> None:
    print("Loading data for")
    for key in ["handle", "contest_id", "problem_id", "verdict", "language"]:
        print(f"\t{key}:", getattr(args, key, None) or "ANY")

    os.makedirs(args.handle, exist_ok=True)

    api_client = CodeforcesAPIClient()

    contest_list = [
        c for c in api_client.contest_list()
        if args.contest_id is None or c.id == args.contest_id
    ]

    available_contests = []
    submissions = api_client.user_status(args.handle)

    submitted_contest_ids = list(
        set(s.contestId for s in submissions if s.contestId in contest_list)
    )
    submitted_problems_ids = list(
        set((s.contestId, s.problem.index) for s in submissions if s.contestId in contest_list)
    )
    contest_ids = submitted_contest_ids if args.contest_id is None else [args.contest_id]

    for i, contest_id in enumerate(contest_ids):
        print(f"Downloading tests for contest: {contest_id}")
        real_contest, problems = api_client.contest_standings(contest_id)

        if real_contest is None:
            logging.warning(F"Contest {contest_id} is not available. Skip.")
            continue
        available_contests.append(real_contest)

        available_problems = [
            p for p in problems
            if (
                p.index == args.problem_id or
                (args.contest_id and args.problem_id is None) or
                (
                    args.contest_id is None and
                    args.problem_id is None and
                    (p.contestId, p.index) in submitted_problems_ids
                )
            )
        ]

        for problem in available_problems:
            print(f"\tDownloading tests for problem: {contest_id}{problem.index}")
            path = f"{args.handle}/{real_contest.id}/{problem.index}/tests"
            tests = api_client.scrape_sample_tests(problem)
            os.makedirs(path, exist_ok=True)
            for i, (input_text, output_text) in enumerate(tests, start=1):
                os.makedirs(f"{path}/sample_{i}", exist_ok=True)
                with open(f"{path}/sample_{i}/input.txt", "w") as file:
                    file.write(input_text)
                with open(f"{path}/sample_{i}/output.txt", "w") as file:
                    file.write(output_text)

    for (contestId, index), submissions in groupby(
        submissions,
        key=lambda s: (s.contestId, s.problem.index),
    ):
        if contestId not in available_contests:
            continue

        if args.problem_id and index != args.problem_id:
            continue

        print(f"Downloading submissions for problem: {contestId}{index}")
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
                if s.id > (latest_submission_id or 0):
                    latest_submission_id = s.id
                download_submission(api_client, s, path, rewrite=args.force)

            if verdict == Verdict.OK and latest_submission_id:
                solution_path = (
                    f"{args.handle}/{contestId}/{index}/{contestId}{index}.{lang2ext(language)}"
                )
                if not os.path.exists(solution_path):
                    shutil.copy(
                        f"{path}/{latest_submission_id}/"
                        f"{latest_submission_id}.{lang2ext(language)}",
                        solution_path
                    )
