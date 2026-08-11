import argparse
import re
from collections import Counter
import json
import datetime

# build the parser
parser = argparse.ArgumentParser(description='Reads a log file and returns various error stats')
parser.add_argument('--file', '-f', required=True, help='the log file to analyze')
parser.add_argument('--level', '-l', nargs='?', default='ERROR', const='ERROR', type=str.upper, choices=['ERROR', 'WARN', 'INFO'], help='Default is ERROR if none is provided')
parser.add_argument('--version', '-v', action='version', version='%(prog)s v0.5')
parser.add_argument('--top5', '-t', action='store_true', help='Show the top 5 most frequent messages')
parser.add_argument('--json', '-j', action='store_true', help='Convert the log file to JSON and print it')
parser.add_argument('--since', '-s', type=datetime.date.fromisoformat, help='Display logs since given date (YYYY-MM-DD)')

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

def convert_to_json(filename):
    log_pattern = re.compile(
        r"^(?P<date>\d{4}-\d{2}-\d{2}) "
        r"(?P<time>\d{2}:\d{2}:\d{2}) "
        r"\[(?P<level>[A-Za-z]+)\] "
        r"(?P<message>.+)$"
    )

    entries = []

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            match = log_pattern.match(line)
            if match:
                entries.append(match.groupdict())

    return json.dumps(entries, indent=2)

def find_logs_since(filename, filter_date):
    date_format = "%Y-%m-%d"
    target_date = datetime.datetime.strptime(str(filter_date), date_format)
    filter_pattern = re.compile(r"^(\d{4}-\d{2}-\d{2})")

    matching_lines = []

    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            match = filter_pattern.match(line)
            if match:
                log_date_str = match.group(1)
                try:
                    log_date = datetime.datetime.strptime(log_date_str, date_format)

                    if log_date >= target_date:
                        matching_lines.append(line)
                except ValueError:
                    continue

    return matching_lines


def main():
    if args.top5:
        cleaned_log = top_five(args.file)
        print ("Here are the Top 5 Most Common lines in your log:\n")
        for (message,count) in cleaned_log:
            print(f"[Occurrences: {count}] {message}")

    elif args.json:
        json_output = convert_to_json(args.file)
        print(json_output)

    elif args.since:
        date_to_search = args.since
        filtered_dates = find_logs_since(args.file, date_to_search)

        if not filtered_dates:
            print(f"No log entries found on or after {args.since}!")

        else:
            for line in filtered_dates:
                print(line)            

    else:
        log_level = args.level
        total_lines, matching_line_count = analyze_file(args.file, log_level)
        print(f'Total lines in file: {total_lines}')
        print(f'Lines matching log level {log_level.upper()}: {matching_line_count}')

    return 0


if __name__ == "__main__":
    main()