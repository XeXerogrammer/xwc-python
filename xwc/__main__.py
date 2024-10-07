import argparse
from os.path import getsize
from sys import stdin

def main():

    version_text = """Version: 1.0 - 2024

This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.

Written by: xexerogrammer"""

    parser = argparse.ArgumentParser(description="Print newline, word, and byte counts for each FILE, and a total line if\nmore than one FILE is specified.  A word is a non-zero-length sequence of\nprintable characters delimited by white space.")

    parser.add_argument("-l", "--lines", action="store_true", help="print the newline counts")
    parser.add_argument("-t", "--total", action="store_true", help="print a line with total counts")
    parser.add_argument("-c", "--bytes", action="store_true", help="print the byte counts")
    parser.add_argument("-w", "--words", action="store_true", help="print the word counts")
    parser.add_argument("-L", "--max-line-length", action="store_true", help="print the maximum display width")
    parser.add_argument("-m", "--chars", action="store_true", help="print the character counts")
    parser.add_argument("-v", "--version", action="store_true", help="output version information and exit")
    parser.add_argument("FILE", type=str, nargs="*")

    args = parser.parse_args()

    if args.version:
        print(version_text)
        return 0
    state = get_state(args)
    if args.FILE:
        total_details = {
                    "lines": 0,
                    "words": 0,
                    "chars": 0,
                    "bytes": 0,
                    "longest": 0,
                }
        for file in args.FILE:
            file_details = get_file_details(file)
            if file_details["lines"] < 0:
                continue
            for k in total_details:
                total_details[k] += file_details[k]
            print_report(file, file_details, state)
        if state & 32:
            print_report("total", total_details, state)
    else:
        stdin_details = get_stdin_details()
        print_report("", stdin_details, state)
    return 0

def get_state(args):
    # return an integer corrispomding to the state of the program
    # 1 get lines
    # 2 get words
    # 4 get characters
    # 8 get bytes
    # 16 get longest line
    # 32 show the total
    total = 1 if args.total else 0
    state = 0;
    if args.lines:
        state ^= 1
    if args.words:
        state ^= 2
    if args.chars:
        state ^= 4
    if args.bytes:
        state ^= 8
    if args.max_line_length:
        state ^= 16
    return (state if state else 7) ^ (32 * total)

def get_file_details(fh):
    file_details = {
                    "lines": 0,
                    "words": 0,
                    "chars": 0,
                    "bytes": 0,
                    "longest": 0,
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
        line_chars = 0
        if line[-1] == "\n":
            file_details["lines"] += 1;
        for character in line:
            file_details["chars"] += 1
            if character != "\n":
                line_chars += 1
            if not character.isspace():
                in_word = True
            elif in_word == True:
                in_word = False
                file_details["words"] += 1
        if in_word:
            in_word = False
            file_details["words"] += 1
        if line_chars > file_details["longest"]:
            file_details["longest"] = line_chars

    file_details["bytes"] = getsize(fh)
    return file_details

def get_stdin_details():
    data = stdin.read()
    stdin_details = {
                    "lines": 0,
                    "words": 0,
                    "chars": 0,
                    "bytes": 0,
                    "longest": 0,
                }

    in_word = False
    lines = [x for x in data.split("\n")]
    for line in lines:
        line_chars = 0  
        for character in line:
            stdin_details["chars"] += 1
            if character != "\n":
                line_chars += 1
            if not character.isspace():
                in_word = True
            elif in_word == True:
                in_word = False
                stdin_details["words"] += 1
        if in_word:
            in_word = False
            stdin_details["words"] += 1
        if line_chars > stdin_details["longest"]:
            stdin_details["longest"] = line_chars
    stdin_details["lines"] = len(lines) - 1
    stdin_details["chars"] += len(lines) - 1
    stdin_details["bytes"] = len(data.encode("utf-8"))
    return stdin_details

def print_report(file, file_details, state):
    if state & 1:
        print(f'{file_details["lines"]:4}', end=" ")
    if state & 2:
        print(f'{file_details["words"]:4}', end=" ")
    if state & 4:
        print(f'{file_details["chars"]:4}', end=" ")
    if state & 8:
        print(f'{file_details["bytes"]:4}', end=" ")
    if state & 16:
        print(f'{file_details["longest"]:4}', end=" ")
    print(file)

main()
