import os
import argparse


class Parser(argparse.ArgumentParser):

    def __init__(self):
        super(Parser, self).__init__()

    @staticmethod
    def optparse():
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "dir", default=os.getcwd(), nargs="?",
            help="Pass a directory to create the .gitignore for (*default: current)"
        )
        parser.add_argument(
            "-s", "--skip", default=[], nargs="+", dest="skipFiles",
            help="Pass a list of files to skip over during scanning"
        )
        return parser.parse_args()