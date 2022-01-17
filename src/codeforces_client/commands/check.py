from argparse import Namespace
from difflib import ndiff
import logging
import os
from colorama import Fore
import stat
import subprocess

from codeforces_client.utils.lang2ext import lang2ext


def get_solution_exec_path(args: Namespace) -> str:
    if args.solution_path:
        if not os.path.exists(args.solution_path):
            raise FileNotFoundError("Solution file was not found.")
        solution_path = args.solution_path
    else:
        if not (args.handle and args.contest_id):
            raise FileNotFoundError("Specify `--solution-path` or `--handle` and `--contest-id`")
        solution_path = f"{args.handle}/{args.contest_id}"
        if not args.problem_id:
            raise NotImplementedError(
                "Current implementation does not support check for the whole contest. "
                "Please, specify `--problem-id`"
            )
        solution_path = f"{solution_path}/{args.problem_id}"
        solution_file_mask = f"{solution_path}/{args.contest_id}{args.problem_id}*"
        if args.language:
            solution_file_mask = f"{solution_file_mask}.{lang2ext(args.language)}"

        maybe_solutions = [
            file
            for _, _, files in os.walk(solution_path)
            for file in files
            if (file.lower().startswith(f"{args.contest_id}{args.problem_id}".lower())) and
               (args.language is None or file.endswith(f".{lang2ext(args.language)}"))
        ]

        if not maybe_solutions:
            raise FileNotFoundError(
                f"There is no file like {solution_file_mask} found to be used as a solution."
            )

        solution_path = f"{solution_path}/{maybe_solutions[0]}"
        if len(maybe_solutions) > 1:
            logging.warning(f"There are several solutions fitting {solution_file_mask}.")

    print(f"Solution file to check: {solution_path}")

    print("Ensuring that solution file is executable.")
    st = os.stat(solution_path)
    if not st.st_mode & stat.S_IEXEC:
        logging.warning(f"{solution_path} is not executable!.")
        file_extension = solution_path.split(".")[-1]
        if file_extension not in ["py"]:
            raise RuntimeError(
                f"Your solution file is not executable and compilation for {file_extension} "
                f"files is not supported."
            )
        if file_extension == "py":
            logging.warning(f"Making file {solution_path} executable.")
            os.chmod(solution_path, st.st_mode | stat.S_IEXEC)
            with open(solution_path, "r+") as solution_file:
                solution_text = solution_file.read()
                if not solution_text.startswith("#!"):
                    solution_file.seek(0)
                    solution_file.write("#!/usr/bin/env python\n" + solution_text)

    return solution_path


def run(args: Namespace) -> None:
    print("Checking solution for")
    for key in ["handle", "contest_id", "problem_id", "language", "solution_path"]:
        print(f"\t{key}:", getattr(args, key, None))

    solution_path = get_solution_exec_path(args)
    tests_path = f"{args.handle}/{args.contest_id}/{args.problem_id}/tests"

    total_passed = 0
    total_tests = 0
    failed_diffs = {}
    for _, test_dirs, _ in os.walk(tests_path):
        for test_name in test_dirs:
            print(f"Executing test: {test_name}")
            total_tests += 1
            with open(f"{tests_path}/{test_name}/input.txt", "r") as input_data:
                with open(f"{tests_path}/{test_name}/output.txt", "r") as expected_data:
                    pipeline = subprocess.Popen(
                        solution_path,
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        close_fds=True,
                        universal_newlines=True,
                    )
                    real_output, err_output = pipeline.communicate(input_data.read())
                    diff = None
                    expected_lines = [line.rstrip() for line in expected_data.readlines()]
                    real_lines = [line.rstrip() for line in real_output.splitlines()]
                    if expected_lines != real_lines:
                        diff = ndiff(expected_lines, real_lines)
                    if not diff:
                        print(Fore.GREEN + f"Passed: {test_name}" + Fore.RESET)
                        total_passed += 1
                    else:
                        print(Fore.RED + f"Failed: {test_name}" + Fore.RESET)
                        failed_diffs[test_name] = diff

    for test_name in failed_diffs:
        fail_str = "=" * 20 + f" Failed {test_name} " + "=" * 20
        print(Fore.RED + fail_str)
        print("\n".join(failed_diffs[test_name]))
        print(Fore.RED + "=" * len(fail_str) + Fore.RESET)

    if total_tests == total_passed:
        print(
            Fore.GREEN + "=" * 10 +
            f" All tests passed! Passed: {total_passed} / {total_tests} " +
            "=" * 10 + Fore.RESET
        )
    elif total_tests and not total_passed:
        print(
            Fore.RED + "=" * 10 +
            f" All tests failed! Passed: 0 / {total_tests} " +
            "=" * 10 + Fore.RESET
        )
    else:
        print(
            Fore.YELLOW + "=" * 10 +
            f" Not all tests passed! Passed: {total_passed} / {total_tests} " +
            "=" * 10 + Fore.RESET
        )
