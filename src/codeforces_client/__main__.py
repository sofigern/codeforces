import argparse
from itertools import chain
import logging

from codeforces_client import VERSION
from codeforces_client.api.verdict import Verdict
from codeforces_client.commands.config import get_default_config, run as config
from codeforces_client.commands.load import run as load
from codeforces_client.commands.check import run as check


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", "-V", action="version", version=f"%(prog)s {VERSION}")
    parser.add_argument(
        '-d', '--debug',
        help="Print lots of debugging statements",
        action="store_const", dest="loglevel", const=logging.DEBUG,
        default=logging.WARNING,
    )

    default_config = dict(get_default_config().items("DEFAULT"))
    parser.set_defaults(**default_config)

    subparsers = parser.add_subparsers()

    # Common arguments can't be provided as parent parsers due to
    # https://bugs.python.org/issue22401
    # So this old days workaround with collections of argument params is used.

    problem_params = [
        # args, kwargs
        (["--contest-id"], dict(type=int, help="Codeforces contest-id.")),
        (["--problem-id"], dict(help="Codeforces problem index. i.e. `A` or `B`"))
    ]

    solution_params = [
        (["--handle"], dict(help="Codeforces user handle.")),
        (
            ["--language"],
            dict(default="ANY", help="Programming language. Use `any` to not specify.")
        )
    ]

    load_parser = subparsers.add_parser(
        "load",
        help="Load data from Codeforces.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    for args, kwargs in chain(problem_params, solution_params):
        load_parser.add_argument(*args, **kwargs)

    load_parser.add_argument(
        "--verdict",
        type=Verdict,
        default=Verdict.OK,
        help="Load only submissions with chosen `verdict`. Choose `ALL` to suppress this filter.",
        choices=list(Verdict),
    )
    load_parser.add_argument(
        "--force", "-f", action='store_true', default=False,
        help="Rewrite already existing files."
    )
    load_parser.set_defaults(func=load, **default_config)

    check_parser = subparsers.add_parser(
        "check",
        help="Check solutions returning correct answers for tests.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    for args, kwargs in chain(problem_params, solution_params):
        check_parser.add_argument(*args, **kwargs)

    check_parser.add_argument(
        "--solution-path",
        help="Custom path to the solution executive file."
    )
    check_parser.set_defaults(func=check, **default_config)

    config_parser = subparsers.add_parser(
        "config", help="Configurate client defaults.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    config_parser.add_argument(
        "--file", "-f", default="~/.cf-cli.ini",
        help=
            "If not set explicitly with --file, there are two files where cf-cli config "
            "will search for configuration options:\n"
            "\t~/.cf-cli.ini User-specific configuration file. [Default]\n"
            "\t/etc/cf-cli/config.ini System-wide configuration file."
    )
    config_parser.set_defaults(func=config, **default_config)

    args = parser.parse_args()
    if getattr(args, "language", "").lower() == 'any':
        args.language = None

    logging.basicConfig(level=args.loglevel)
    args.func(args)


if __name__ == '__main__':
    run()
