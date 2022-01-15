from argparse import Namespace
from configparser import ConfigParser
import getpass
import os
from typing import Optional, Callable


def get_default_config() -> ConfigParser:
    parser = ConfigParser()
    parser.read([
        os.path.expanduser(path) for path in [
            "/etc/cf-cli/config.ini",
            "~/.cf-cli.ini",
        ]
    ])

    return parser


def input_dialogue(description: str, default: Optional[str] = None) -> Optional[str]:
    print(f"Enter your codeforces {description} [{default}]: ", end="")
    return input()


def secure_input_dialogue(description: str, default: Optional[str] = None) -> Optional[str]:
    short_default_str = None
    if default:
        short_default_str = default[:4] + '*****' + default[-4:]
    return getpass.getpass(f"Enter your codeforces {description} [{short_default_str}]: ")


def init_config(
        parser: ConfigParser,
        name: str,
        description: str,
        dialogue: Callable = input_dialogue,
):
    config = parser.get("DEFAULT", name, fallback=None)
    in_config = dialogue(description, default=config)
    if in_config:
        if in_config.lower() == "erase":
            parser.remove_option("DEFAULT", name)
            config = None
        else:
            config = in_config

    if config:
        parser.set(None, name, config)


def run(args: Namespace) -> None:
    config = get_default_config()
    print("Enter `erase` to just erase the config value.")
    with open(os.path.expanduser(args.file), "w+") as cfgfile:
        init_config(config, "handle", "handle")
        init_config(config, "language", "programming language")
        init_config(config, "api_token", "API token", dialogue=secure_input_dialogue)
        config.write(cfgfile)
