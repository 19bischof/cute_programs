import pathlib


def dir_parse(path, depth=0):
    """Parses Directory and outputs in a Tree.
    :param path: Pathlike Object
    :param entry: has to be called with depth = 0 or not specified"""

    p = pathlib.Path(path)
    # if depth == 2:  #to get just a shallow view
    #     return
    for new in p.glob("*"):  # get all objects in directory
        print("    " * depth, end="")  # indent
        if depth != 0:
            print("|___ ", end="")  # tree structure
        print(new.name)
        if new.is_dir():
            dir_parse(new, depth + 1)  # recursion with increased depth


def all_files_from_dir(path, files=[]):
    """Is a recursion function to measure all the files in a directory
    :param path : pathlike Object
    :param files : no need to specify but you can do that. FileTuples are appended to files
    return: list of Tuples [(name,size in Bytes)]"""

    p = pathlib.Path(path)
    for new in p.glob("*"):  # get all objects in directory
        if new.is_dir():
            all_files_from_dir(new, files)
        else:
            stat = new.stat()
            files.append((str(new.as_posix()), stat.st_size))
    files = sorted(files, key=lambda tup: tup[1])
    return files


def pretty_print_files(files):
    """Outputs files from 'all_files_from_dir'.
    Has to be called explicitly!
    :param files: list of Tuples [(name,size in Bytes)]"""

    sizes = (
        "B",
        "KB",
        "MB",
        "GB",
        "TB",
        "PB",
    )  # factor is 1024 because its widely used in os's
    for l in files:
        dim = 0
        while 1024 ** (dim + 1) < l[1]:  # get unit index (Byte, Kilobyte, ...)
            dim += 1
        # scientific notation, because no trailing zeroes
        size_str = ("{:5.4g} {}").format(l[1] / 1024**dim, sizes[dim])
        # only show the last 40 characters of name or pad to 40
        name_str = l[0][:-40:-1][::-1].ljust(40)
        name_str = "{{depth:{:02d}}} {}".format(
            l[0].count("/") - 1, name_str)  # show depth
        print("{}: {}".format(name_str, size_str))


if __name__ == "__main__":
    paths = []
    paths.append(pathlib.Path(__file__).absolute().parent.parent.parent.parent)

    for path in paths:
        lot = all_files_from_dir(path)
        pretty_print_files(lot)
        print(f"# All files from {path}")
