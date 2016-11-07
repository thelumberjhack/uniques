# coding: utf-8
import os
import sys
import argparse

from uniques import list_files, get_uniques


class Unique(object):

    @staticmethod
    def parse_args():
        """ Command line arguments parser.

        :return: parsed arguments.
        """
        parser = argparse.ArgumentParser(
            prog="unique",
            description="Tool to get unique files only based on their sha256 hash.",
            epilog="returns 0 on success, -1 otherwise."
        )

        parser.add_argument("-i", "--input", dest="input", type=str, help="input folder to triage", required=True)
        parser.add_argument("-o", "--output", dest="output", type=str, help="output folder to store unique files",
                            required=True)
        parser.add_argument("-e", "--file-ext", dest="file_extension", type=str, help="unique file extension",
                            required=True)
        parser.add_argument("-p", "--pattern", dest="pattern", type=str, default="id*", help="file pattern filter")

        return parser.parse_args()

    @classmethod
    def main(cls):
        """ Main tool function.

        :return: 0 on success, -1 otherwise
        """
        args = cls.parse_args()

        output_dir = ""
        file_ext = "." + args.file_extension
        pattern = args.pattern

        if not os.path.exists(args.input) or not os.path.isdir(args.input):
            print("[-] {} does not exist or is not a directory".format(args.input))
            return -1

        else:
            input_dir = os.path.abspath(args.input)

        corpus = list_files(input_dir, pattern=pattern)
        total = len(corpus)
        print("[+] Found {} files.".format(total))

        output_dir = os.path.abspath(args.output)
        if not os.path.exists(output_dir):
            print("[+] Creating {} output directory".format(output_dir))
            os.mkdir(output_dir)

        print("[+] Starting triage of the files... This might take a while.")
        count = get_uniques(corpus, output_dir, file_ext)
        print("[+] Done copying {}/{} unique files".format(count, total))

        return 0


def main():
    """ Console script entry point """
    sys.exit(Unique.main())


if __name__ == '__main__':
    main()
