#!/usr/bin/python

class Dir:
    """Information about a directory; the path and the combined size and amount of the included files."""

    def __init__(self, path, size, filecount):
        self.path = path
        self.size = size
        self.filecount = filecount

    def __cmp__(self, other):
        return cmp(self.size, other.size)

    def getSize(self, precision=3):
        """Get size of directory entries, with correct size abbreviation suffix, rounded down to precision."""
        kilo = 1000.0
        if self.size < kilo:
            return str(self.size) + " B"
        elif self.size < kilo ** 2:
            return str(round(self.size / kilo, precision)) + " kB"
        elif self.size < kilo ** 3:
            return str(round(self.size / (kilo ** 2), precision)) + " MB"
        elif self.size < kilo ** 4:
            return str(round(self.size / (kilo ** 3), precision)) + " GB"
        else:
            return str(round(self.size / (kilo ** 4), precision)) + " TB"

    def printSizeInfo(self):
        return self.getSize() + "\t" + self.path + "\t" + str(self.filecount) + " files"

if __name__ == "__main__":
    # def get_arguments(self):
    # from optparse import OptionParser
    # parser = OptionParser()
    # parser.add_option("-n", "--show-number", action="store_true", dest="checkout",
    #                      help="Checkout a clean working copy before performing operations.")
    #    parser.set_default("checkout", False)
    #    parser.add_option("--show-macros", action="callback", callback=show_macros_callback,
    #                      help="Show all URL macros and exit.")
    #    parser.set_default("checkout", False)
    #    (options, args) = parser.parse_args()
    #    checkout=options.checkout

    #    # The working copy is always the final argument
    #    if len(args) > 0:
    #        workingCopy=args[-1]
    #        if len(args) == 3:
    #            source=expand_macro(args[0])
    #            target=expand_macro(args[1])

    from os import access, getcwdu, R_OK, walk
    from sys import argv
    from os.path import join, getsize

    dir_sizes = []
    # Walk arg 1, or pwd in no arg supplied.
    cwdu = getcwdu()
    for root, dirs, files in walk(argv[1] if len(argv) > 1 else cwdu):
        file_sizes = 0
        file_count = 0
        for name in files:
            full_path = join(root, name)
            if access(full_path, R_OK):
                file_sizes += getsize(full_path)
                file_count += 1

        dir = Dir(root.replace(cwdu, ''), file_sizes, file_count)
        dir_sizes.append(dir)

    dir_sizes.sort(reverse=True)
    # Show top max arg 2 entries, or 10 if no arg supplied.
    for dir in dir_sizes[0:int(argv[2] if len(argv) > 2 else 10)]:
        print dir.printSizeInfo()
