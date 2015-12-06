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


if __name__ == "__main__":
    sizes = []
    # def get_arguments(self):
    # from optparse import OptionParser
    # parser = OptionParser()
    #    parser.add_option("-n", "--show-number", action="store_true", dest="checkout",
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

    # Walk arg 1, or pwd in no arg supplied.
    for root, dirs, files in walk(argv[1] if len(argv) > 1 else getcwdu()):
        sizes.append(Dir(root,
                         sum(getsize(join(root, name)) for name in files if access(join(root, name), R_OK)),
                         len(files)))

    sizes.sort(reverse=True)
    # Show top max arg 2 entries, or 10 if no arg supplied.
    for k in sizes[0:int(argv[2] if len(argv) > 2 else 10)]:
        print k.getSize() + "\t" + k.path + "\t" + str(k.filecount) + " files"
