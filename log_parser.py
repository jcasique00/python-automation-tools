import argparse
import re

# build the parser
parser = argparse.ArgumentParser(description='Reads a log file and returns various error stats')
parser.add_argument('--file', '-f', required=True, help='the log file to analyze')
parser.add_argument('--level', '-l', help='ERROR|WARN|INFO')
parser.add_argument('--version', '-v', action='version', version='%(prog)s v0.1')

args = parser.parse_args()

def file_line_counter(filename):
    line_count=0
    with open(filename) as f:
        lines = f.readlines()

    for line in lines:
        line_count +=1

    return line_count

def log_level(filename, level=None):
    if level is None:
        level = 'error'
    with open(filename) as f:
        lines = f.readlines()
        hit_count=0
        for line in lines:
            if re.search(level, line, re.IGNORECASE):
                hit_count +=1

    return hit_count

def main():
    total_lines = file_line_counter(args.file)

    if args.level:
        matching_line_count = log_level(args.file, args.level)
        

    print(f'Total lines in file: {total_lines}')
    print(f'Lines matching log level {args.level.upper()}: {matching_line_count}')
    return 0


if __name__ == "__main__":
    main()