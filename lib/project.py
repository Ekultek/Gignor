import os
import shutil
import datetime

import requests

from lib.settings import (
    COLLECTIONS_DOWNLOAD_LINK,
    TEMP_CACHE_DIR,
    random_string,
    CACHE_DIR,
    GITIGNORE_GIGNOR_IDENTIFIER
)


class Checker(object):

    decisions = None
    workable_links = None
    cache_dir = "{}/{}".format(TEMP_CACHE_DIR, str(datetime.datetime.today()).split(" ")[0])

    def __init__(self, regex, directory, skip_files):
        self.regex = regex
        self.directory = directory
        self.skip = skip_files

    def __cleanup(self):
        shutil.rmtree(self.cache_dir, ignore_errors=True)

    def __decide(self):
        retval = set()
        files = os.listdir(self.directory)
        for f in files:
            if f not in self.skip:
                for re in self.regex:
                    if re[1].search(f) is not None:
                        retval.add(re[0])
        return retval

    def __create_manifest(self):
        retval = set()
        for item in self.decisions:
            for link in COLLECTIONS_DOWNLOAD_LINK:
                if not link.endswith("/"):
                    url = link + "/{}.gitignore".format(item)
                    try:
                        req = requests.get(url, timeout=2)
                    except:
                        req.status_code = 999

                    if req.status_code == 200:
                        retval.add(url)
        return retval

    def download_gitignore(self):
        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)
        self.decisions = self.__decide()
        self.workable_links = self.__create_manifest()
        if len(self.workable_links) != 0:
            for item in self.workable_links:
                try:
                    req = requests.get(item, timeout=2)
                except:
                    req = None
                if req is not None:
                    file_path = "{}/{}".format(self.cache_dir, item.split("/")[-1])
                    with open(file_path, "a+") as tmp:
                        tmp.write(req.content)
            dest_file = "{}/{}".format(
                CACHE_DIR,
                str(datetime.datetime.today()).split(" ")[0] + "." + random_string() + ".gitignore"
            )
            open(dest_file, "a+").write(GITIGNORE_GIGNOR_IDENTIFIER)
            for item in os.listdir(self.cache_dir):
                with open("{}/{}".format(self.cache_dir, item), "a+") as source:
                    with open(dest_file, "a+") as dest:
                        dest.write(source.read())
            shutil.copyfile(dest_file, "{}/.gitignore".format(os.getcwd()))
            self.__cleanup()
            return dest_file
        else:
            return None


