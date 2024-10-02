import argparse

def main():

    version_text = """Version: 1.0 - 2024

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by: xexerogrammer"""

    parser = argparse.ArgumentParser(description="Print newline, word, and byte counts for each FILE, and a total line if\nmore than one FILE is specified.  A word is a non-zero-length sequence of\nprintable characters delimited by white space.")

    parser.add_argument("-l", "--lines", action="store_true", help="print the newline counts")
    parser.add_argument("-w", "--words", action="store_true", help="print the word counts")
    parser.add_argument("-v", "--version", action="store_true", help="output version information and exit")
    parser.add_argument("FILE", type=str, nargs="*")

    args = parser.parse_args()

    if args.version:
        print(version_text)
        return 0
    state = get_state(args)
    for file in args.FILE:
        file_details = get_file_details(file)
        if file_details["lines"] < 0:
            continue
        print_report(file, file_details, state)
    return 0

def get_state(args):
    # return an integer corrispomding to the state of the program
    # 1 get lines
    # 2 get words
    state = 0;
    if args.lines:
        state ^= 1
    if args.words:
        state ^= 2
    return state

def get_file_details(fh):
    file_details = {
                    "lines": 0,
                    "words": 0,
                }
    file = None
    in_word = False
    try:
        file = open(fh, "r")
    except Exception:
        print(fh, ": no such file or directory")
        file_details["lines"] = -1
        return file_details

    for line in file:
        file_details["lines"] += 1;
        for character in line:
            if not character.isspace():
                in_word = True
            elif in_word == True:
                in_word = False
                file_details["words"] += 1

    return file_details

def print_report(file, file_details, state):
    if state & 1:
        print(f'{file_details["lines"]:4}', end=" ")
    if state & 2:
        print(f'{file_details["words"]:4}', end=" ")
    print(file)

main()
