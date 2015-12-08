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

if __name__ == "__main__":
    from docopt import docopt
    from os import access, getcwdu, R_OK, walk
    from os.path import join, getsize

    documentation = """Expose hogdirs
    Usage:
      hogdirs.py [PATH]
      hogdirs.py [PATH AMOUNT_SHOWN]
      hogdirs.py (-h | --help)

    Arguments:
      PATH          A file path examine. Defaults to current working directory.
      AMOUNT_SHOWN  The amount of directory entries to show. Defaults to 10.

    Options:
      -h --help     Show this screen.
    """
    arguments = docopt(documentation)
    print(arguments)

    current_dir = getcwdu()
    path_to_examine = arguments['PATH'] if arguments['PATH'] is not None else current_dir
    amount_to_show = arguments['AMOUNT_SHOWN'] if arguments['AMOUNT_SHOWN'] is not None else 10

    dir_sizes = []
    for root, dirs, files in walk(path_to_examine):
        file_sizes = 0
        file_count = 0
        for name in files:
            full_path = join(root, name)
            if access(full_path, R_OK):
                file_sizes += getsize(full_path)
                file_count += 1

        dir = Dir(makePathRelative(current_dir, root), file_sizes, file_count)
        dir_sizes.append(dir)

    dir_sizes.sort(reverse=True)
    # Show top max arg 2 entries, or 10 if no arg supplied.
    for dir in dir_sizes[0:int(amount_to_show)]:
        print dir.printSizeInfo()
