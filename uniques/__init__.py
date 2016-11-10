# coding: utf-8
import os
import sys
import shutil
import multiprocessing
from hashlib import sha256
from fnmatch import filter


class Hasher(multiprocessing.Process):

    def __init__(self, task_queue, result_queue):
        """
        :param task_queue:
        :param result_queue:
        """
        super(Hasher, self).__init__()
        self.task_queue = task_queue
        self.result_queue = result_queue

    def run(self):
        """
        """
        while True:
            file_name = self.task_queue.get()
            with open(file_name, "rb") as fh:
                digest = sha256(fh.read()).hexdigest()

            self.result_queue.put((file_name, digest))

        return


def list_files(input_dir, pattern):
    """ List all files (recursively) from '_input' folder, filtered by 'pattern'.

    :param input_dir: input folder
    :type input_dir: str
    :param pattern: filter
    :type pattern: str
    :return: list of the paths to the filtered files
    """
    if not os.path.isdir(input_dir):
        print("[-]{} is not a directory".format(input_dir))
        raise Exception("{} is not a directory".format(input_dir))

    print("[+] Listing files from: {}".format(input_dir))

    items = []
    corpus_path = os.path.abspath(input_dir)
    for root, dir_names, file_names in os.walk(corpus_path):
        for filename in filter(file_names, pattern):
            items.append(os.path.join(root, filename))

    return items


def print_progress(iteration, total, prefix="", suffix="", decimals=1, bar_length=100):
    """ Console progress bar.
    Original code from https://stackoverflow.com/a/34325723

    :param iteration: current iteration
    :type iteration: int
    :param total: total iterations
    :type total: int
    :param prefix: prefix string
    :type prefix: str
    :param suffix: suffix string
    :type suffix: str
    :param decimals: positive number of decimals in percent complete
    :type decimals: int
    :param bar_length: character length of bar
    :type bar_length: int
    """
    format_str = "{0:." + str(decimals) + "f}"
    percents = format_str.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = "█" * filled_length + "-" * (bar_length - filled_length)
    sys.stdout.write("\r%s |%s| %s%s %s" % (prefix, bar, percents, "%", suffix)),
    if iteration == total:
        sys.stdout.write("\n")
    sys.stdout.flush()


def get_uniques(files, output_dir, file_extension):
    """ Browse `files` list and copies unique files to `output_dir` based on their sha256 hash
    and print progress.

    :param files: input files list
    :type files: list
    :param output_dir: unique files directory
    :type output_dir: str
    :param file_extension: file extension to be appended to unique file
    :type file_extension: str
    :return: number of unique files copied
    """
    uniques = {}
    count = 0
    prog_count = 0
    total = len(files)

    print_progress(prog_count, total, prefix="[*] Progress:", suffix="Complete", bar_length=50)
    for _file in files:
        with open(_file, "rb") as fh:
            hashed = sha256(fh.read()).hexdigest()
        if hashed not in uniques.keys():
            uniques[hashed] = _file[:]
            shutil.copy(_file, os.path.join(output_dir, hashed + file_extension))
            count += 1
        prog_count += 1
        print_progress(prog_count, total, prefix="[*] Progress:", suffix="Complete. [{:08d}/{}]".format(
            count, prog_count
        ), bar_length=50)

    return count
