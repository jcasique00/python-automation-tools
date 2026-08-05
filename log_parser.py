import argparse
import re
from collections import Counter

# build the parser
parser = argparse.ArgumentParser(description='Reads a log file and returns various error stats')
parser.add_argument('--file', '-f', required=True, help='the log file to analyze')
parser.add_argument('--level', '-l', nargs='?', default='ERROR', const='ERROR', choices=['ERROR', 'WARN', 'INFO'], help='Default is ERROR if none is provided')
parser.add_argument('--version', '-v', action='version', version='%(prog)s v0.2')
parser.add_argument('--top5', '-t', action='store_true', help='Show the top 5 most frequent messages')

args = parser.parse_args()

def analyze_file(filename, level):
    line_count = 0
    hit_count = 0

    with open(filename, "r") as f:
        lines = f.readlines()
        for line in lines:
            line_count += 1
            if re.search(level, line, re.IGNORECASE):
                hit_count +=1

    return line_count, hit_count

def top_five(filename):
    with open(filename, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    # Strip dates and time from the beginning of each line
        date_time = r"^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} "
        no_time_lines = [re.sub(date_time, "", line) for line in lines]
        
    # Normalize data (remove dynamic numbers or IP addresses)
        ip_addr = r"\d+.\d+.\d+.\d+"
        noip_lines = [re.sub(ip_addr, "x.x.x.x", line) for line in no_time_lines]

        port_number = r"port \d+"
        normalized_lines = [re.sub(port_number, "port X", line) for line in noip_lines]

        # Count the frequency of each message
        count_recurrence = Counter(normalized_lines)

        top_five = count_recurrence.most_common(5)

    return top_five

def main():
    if args.level:
        log_level = args.level
           
        total_lines, matching_line_count = analyze_file(args.file, log_level)

        print(f'Total lines in file: {total_lines}')
        print(f'Lines matching log level {log_level.upper()}: {matching_line_count}')
        return 0


    elif args.top5:
        cleaned_log = top_five(args.file)
        print ("Here are the Top 5 Most Common lines in your log:\n")
        for (message,count) in cleaned_log:
            print(f"[Occurrences: {count}] {message}")

    else:
        total_lines, matching_line_count = analyze_file(args.file, log_level)
        print(f'Total lines in file: {total_lines}')


if __name__ == "__main__":
    main()