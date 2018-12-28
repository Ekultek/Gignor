import os
import re
import json
import string
import random
import datetime

import requests


CONF_DOWNLOAD_LINK = (
    "https://gist.githubusercontent.com/"
    "Ekultek/92defc0cb58d053fc3eedd400c1cf58a/"
    "raw/5033584235a82e9f6fad89c147abef65d5a482df/conf.json"
)
VERSION = "0.1"
BANNER = """
Gignor ~~> v{}
""".format(VERSION)
CUR_DIR = os.getcwd()
HOME = "{}/.gignor".format(os.path.expanduser("~"))
CACHE_DIR = "{}/.cache".format(HOME)
CONF_FILE_LOCATION = "{}/conf.json".format(HOME)
TEMP_CACHE_DIR = "{}/.tmp".format(CACHE_DIR)
COLLECTIONS_DOWNLOAD_LINK = (
    "https://raw.githubusercontent.com/github/gitignore/master",
    "https://raw.githubusercontent.com/github/gitignore/master/Global",
    "https://raw.githubusercontent.com/github/gitignore/master/community",
    "https://raw.githubusercontent.com/github/gitignore/master/community/embedded/",
    "https://raw.githubusercontent.com/github/gitignore/master/community/Python/",
    "https://raw.githubusercontent.com/github/gitignore/master/community/PHP",
    "https://raw.githubusercontent.com/github/gitignore/master/community/Linux",
    "https://raw.githubusercontent.com/github/gitignore/master/community/JavaScript",
    "https://raw.githubusercontent.com/github/gitignore/master/community/Java",
    "https://raw.githubusercontent.com/github/gitignore/master/community/Golang",
    "https://raw.githubusercontent.com/github/gitignore/master/community/Elixir",
    "https://raw.githubusercontent.com/github/gitignore/master/community/DotNet"
)
GITIGNORE_GIGNOR_IDENTIFIER = """# this .gitignore was generated using `gignor` (https://github.com/ekultek/gignore)
# generation occurred on {}.

# gignor created files
.gitignore.bak
.idea/*

""".format(datetime.datetime.today())


def check_for_file(directory, target=".gitignore"):
    current_files = os.listdir(directory)
    in_dir = False
    for f in current_files:
        if f == target:
            in_dir = True
    if in_dir:
        import shutil

        shutil.move("{}/{}".format(directory, target), "{}/.gitignore.bak".format(directory))
    return in_dir


def initialize():
    if not os.path.exists(HOME):
        os.makedirs(HOME)
        os.makedirs(CACHE_DIR)
        os.makedirs(TEMP_CACHE_DIR)
    if not os.path.exists(CONF_FILE_LOCATION):
        with open(CONF_FILE_LOCATION, "a+") as conf:
            req = requests.get(CONF_DOWNLOAD_LINK)
            conf.write(req.content)


def build_regex(config):
    retval = []
    with open(config) as conf:
        data = json.loads(conf.read())
        version_number = data["__version"]
        for item in data["ext"]:
            identifier = item.keys()[0]
            regex_list = item[identifier]
            for regex in regex_list:
                regex = re.compile(regex)
                retval.append((identifier, regex))
    return retval


def random_string(length=16, acceptable=string.ascii_letters):
    retval = []
    for _ in range(length):
        retval.append(random.choice(acceptable))
    return "".join(retval)