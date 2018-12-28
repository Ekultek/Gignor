from lib.project import Checker
from lib.args import Parser
from lib.settings import (
    build_regex,
    initialize,
    CONF_FILE_LOCATION,
    BANNER,
    check_for_file
)


try:
    raw_input
except:
    input = raw_input


def main():
    try:
        print(BANNER)
        opts = Parser().optparse()
        initialize()
        file_check = check_for_file(opts.dir)
        if file_check:
            print(".gitignore already exists in the directory, it has been backed up as .gitignore.bak")
        print("building expressions")
        expressions = build_regex(CONF_FILE_LOCATION)
        print("expressions built, checking files")
        if len(opts.skipFiles) != 0:
            print("a total of {} files will be skipped".format(len(opts.skipFiles)))
        results = Checker(expressions, opts.dir, opts.skipFiles).download_gitignore()
        if results is not None:
            print("downloaded into {}".format(opts.dir))
            print("a copy of this gitignore was saved under {}".format(results))
        else:
            print("unable to determine project structure")
    except KeyboardInterrupt:
        print("user quit")
    except Exception as e:
        print("hit an unhandled exception: {}".format(e))