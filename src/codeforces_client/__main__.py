import argparse
import logging

from codeforces_client import VERSION
from codeforces_client.api.verdict import Verdict
from codeforces_client.commands.config import get_default_config, run as config
from codeforces_client.commands.load import run as load


def run():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
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

    load_parser = subparsers.add_parser(
        "load",
        help="Load data from Codeforces.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    load_parser.add_argument("--handle", help="Codeforces user handle.")
    load_parser.add_argument("--contest-id", type=int, help="Codeforces contest-id.")
    load_parser.add_argument(
        "--language", default="ANY",
        help="Programming language. Use `any` to not specify."
    )
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
    logging.basicConfig(level=args.loglevel)
    args.func(args)


if __name__ == '__main__':
    run()
