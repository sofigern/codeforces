import argparse
from configparser import ConfigParser, RawConfigParser
import logging
import os

from codeforces_client import VERSION
from codeforces_client.commands.config import run as config
from codeforces_client.commands.load import run as load


def get_default_config() -> ConfigParser:
    config = ConfigParser()
    config.read([
        os.path.expanduser(path) for path in [
            '/etc/cf-cli/config.ini',
            '~/.cf-cli.ini',
        ]
    ])

    return config


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

    load_parser = subparsers.add_parser("load", help="Load data from Codeforces.")
    load_parser.add_argument("--handle", help="Codeforces user handle.")
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
