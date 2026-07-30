import argparse
import re

# build the parser
parser = argparse.ArgumentParser(description='Reads a log file and returns various error stats')
parser.add_argument('--file', '-f', required=True, help='the log file to analyze')
parser.add_argument('--version', '-v', action='version', version='%(prog)s v0.1')

args = parser.parse_args()

def line_counter(filename):
    line_count=0
    with open(filename) as f:
        lines = f.readlines()

    for line in lines:
        line_count +=1

    return line_count

def line_filter(filename):
    with open(filename) as f:
        lines = f.readlines()
        filter = "error"
        hit_count=0
        for line in lines:
            if re.search(filter, line, re.IGNORECASE):
                hit_count +=1

    return hit_count

def main():
    print(f"Total lines: {line_counter(args.file)}")
    print(f"Errors: {line_filter(args.file)}")
    return 0


if __name__ == "__main__":
    main()