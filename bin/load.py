import argparse
import logging

from codeforces_client.api.client import CodeforcesAPIClient, Verdict


parser = argparse.ArgumentParser()
parser.add_argument("handle", help="Codeforces user handle.")
args = parser.parse_args()

logging.info("Loading data for handle: %s", args.handle)

api_client = CodeforcesAPIClient()
submissions = api_client.user_status(args.handle)
for submission in submissions:
    if submission.verdict is Verdict.OK:
        print(submission.id, submission.problem, submission.contestId)
