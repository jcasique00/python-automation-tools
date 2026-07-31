import argparse
import re

# build the parser
parser = argparse.ArgumentParser(description='Reads a log file and returns various error stats')
parser.add_argument('--file', '-f', required=True, help='the log file to analyze')
parser.add_argument('--level', '-l', help='ERROR|WARN|INFO. Default is ERROR')
parser.add_argument('--version', '-v', action='version', version='%(prog)s v0.2')

args = parser.parse_args()

def analyze_file(filename, level):
    line_count = 0
    hit_count = 0

    with open(filename) as f:
        lines = f.readlines()
        for line in lines:
            line_count += 1
            if re.search(level, line, re.IGNORECASE):
                hit_count +=1

    return line_count, hit_count

def main():
    # If no level is provided the default is ERROR
    log_level = 'error'

    if args.level:
        log_level = args.level
        matching_line_count = analyze_file(args.file, log_level)
        
    total_lines, matching_line_count = analyze_file(args.file, log_level)

    print(f'Total lines in file: {total_lines}')
    print(f'Lines matching log level {log_level.upper()}: {matching_line_count}')
    return 0


if __name__ == "__main__":
    main()