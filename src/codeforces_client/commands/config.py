from argparse import Namespace
from configparser import ConfigParser
import getpass
import os

def run(args: Namespace) -> None:
    with open(os.path.expanduser(args.file), "w+") as cfgfile:
        Config = ConfigParser()

        print("Enter your codeforces handle: ")
        handler = input()
        token = getpass.getpass("Enter your codeforces API token: ")


        Config.set(None, "handle", handler)
        Config.set(None, "api_token", token)
        Config.write(cfgfile)
