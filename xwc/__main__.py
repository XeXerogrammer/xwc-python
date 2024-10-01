import argparse

def main():

    version_text = """Version: 1.0 - 2024

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by: xexerogrammer"""

    parser = argparse.ArgumentParser(description="Print newline, word, and byte counts for each FILE, and a total line if\nmore than one FILE is specified.  A word is a non-zero-length sequence of\nprintable characters delimited by white space.")

    parser.add_argument("-l", "--lines", action="store_true", help="print the newline counts")
    parser.add_argument("-v", "--version", action="store_true", help="output version information and exit")

    args = parser.parse_args()

    if args.version:
        print(version_text)
        return 0

main()
