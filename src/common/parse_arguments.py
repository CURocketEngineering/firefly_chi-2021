'''
parse_arguments.py
'''

import argparse as arg


def parse_arguments() -> "arg.ArgumentParser.NameSpace":
    parser = arg.ArgumentParser(
        description="Argument parsing for extra features"
    )
    parser.add_argument(
        "--gui", "--curses", "-g", "-G",
        default=False, action="store_true"
    )
    parser.add_argument(
        "--sensehat", "--sense_hat", "-s", "-S",
        default=False, action="store_true"
    )
    arguments = parser.parse_args()
    return arguments
