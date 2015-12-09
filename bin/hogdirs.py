#!/usr/bin/python

class Dir:
    """Information about a directory; the path and the combined size and amount of the included files."""

    def __init__(self, path, size, filecount):
        self.path = path
        self.size = size
        self.filecount = filecount

    def __cmp__(self, other):
        return cmp(self.size, other.size)

    def getSize(self, precision=1):
        """Get size of directory entries, with correct size abbreviation suffix, rounded down to precision."""
        kilo = 1000.0
        if self.size < kilo:
            return str(self.size) + "B"
        elif self.size < kilo ** 2:
            return str(round(self.size / kilo, precision)) + "K"
        elif self.size < kilo ** 3:
            return str(round(self.size / (kilo ** 2), precision)) + "M"
        elif self.size < kilo ** 4:
            return str(round(self.size / (kilo ** 3), precision)) + "G"
        else:
            return str(round(self.size / (kilo ** 4), precision)) + "T"

    def printSizeInfo(self):
        return self.getSize() + "\t" + str(self.filecount) + "\t" + self.path

def makePathRelative(current_dir, path):
    if (current_dir == path):
        return "."
    else:
        return path.replace(current_dir, '')

def getDirsToShow(dirs, arguments):
    if arguments['--shown-all']:
        return dirs
    else:
        return dirs[0:int(arguments['--limit'])]

if __name__ == "__main__":
    from docopt import docopt
    from os import access, getcwdu, R_OK, walk
    from os.path import join, getsize

    documentation = """Expose hogdirs
    Usage:
      hogdirs.py [options] [PATH] 
      hogdirs.py (-h | --help)

    Arguments:
      PATH          The file path to examine. Defaults to current working directory.

    Options:
      -h --help                 Show this screen.
      -l COUNT --limit=COUNT    Limit the amount of directories shown [Default: 10]
      -a --shown-all            Do not limit the amount of directories shown.
    """
    arguments = docopt(documentation)
    print(arguments)

    current_dir = getcwdu()
    path_to_examine = arguments['PATH'] if arguments['PATH'] is not None else current_dir

    dirs_found = []
    for root, dirs, files in walk(path_to_examine):
        file_sizes = 0
        file_count = 0
        for name in files:
            full_path = join(root, name)
            if access(full_path, R_OK):
                file_sizes += getsize(full_path)
                file_count += 1

        dir = Dir(makePathRelative(current_dir, root), file_sizes, file_count)
        dirs_found.append(dir)

    dirs_found.sort(reverse=True)
    for dir in getDirsToShow(dirs_found, arguments):
        print dir.printSizeInfo()
