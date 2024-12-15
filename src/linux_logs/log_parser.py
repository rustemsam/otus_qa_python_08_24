import argparse
import json
import os
import re
import tarfile
from collections import Counter, defaultdict


class LogEntry:
    def __init__(
        self,
        ip,
        date,
        method,
        url,
        status,
        length,
        browser,
        time,
        referer,
        username=None,
    ):
        self.ip = ip
        self.date = date
        self.method = method
        self.url = url
        self.status = int(status)
        self.length = int(length) if length != "-" else 0
        self.browser = browser if browser != "-" else None
        self.referer = referer if referer != "-" else None
        self.time = int(time)
        self.username = username

    @classmethod
    def from_log_line(cls, line):
        try:
            regex = r'(?P<ip>\d+\.\d+\.\d+\.\d+) - (?P<username>"?[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}"?|"?[\w\.-]+"?|"") (?:\[(?P<datetime>[\w/]+:\d{2}:\d{2}:\d{2} [^]]+)\])? "(?P<method>\S+) (?P<url>.*?) HTTP/\S+" (?P<status>(?:\d{3}(?: \d{3})*)) (?P<length>\S+) "(?P<referer>.*?)" "(?P<browser>.*?)" (?P<time>\d+)'

            match = re.match(regex, line)
            if match:
                ip = match.group("ip")
                username = match.group("username").strip('"') or None
                date = match.group("datetime")
                method = match.group("method")
                url = match.group("url")
                status = match.group("status")
                length = match.group("length")
                referer = match.group("referer")
                browser = match.group("browser")
                time = match.group("time")

                return cls(
                    ip,
                    date,
                    method,
                    url,
                    status,
                    length,
                    browser,
                    time,
                    referer,
                    username,
                )
            else:
                return None

        except Exception as e:
            print(f"Error processing line: {line} -> {e}")
            return None

    def __str__(self):
        return (
            f"IP: {self.ip}, Username: {self.username}, Date: {self.date}, Method: {self.method}, Url: {self.url}, "
            f"Status: {self.status}, Length: {self.length}, Referer: {self.referer}, "
            f"Browser: {self.browser}, Time: {self.time} ms"
        )

    def __repr__(self):
        return (
            f"LogEntry(ip={self.ip!r}, username={self.username!r}, date={self.date!r}, method={self.method!r}, "
            f"url={self.url!r}, status={self.status!r}, length={self.length!r}, referer={self.referer!r}, "
            f"browser={self.browser!r}, time={self.time!r})"
        )


def untar_file(file_name, extract_to="."):
    try:
        extracted_files = []
        with tarfile.open(file_name) as tar:
            tar.extractall(path=extract_to)
            extracted_files = [
                os.path.join(extract_to, name) for name in tar.getnames()
            ]
        return extracted_files
    except Exception as e:
        return f"An error occurred while extracting {file_name}: {e}"


def check_dir_or_file(file_name):
    print(f"Checking path: {file_name}")  # Debugging
    if os.path.isdir(file_name):
        print(f"{file_name} is a directory.")
        return [
            os.path.join(file_name, f)
            for f in os.listdir(file_name)
            if os.path.isfile(os.path.join(file_name, f))
        ]
    elif os.path.isfile(file_name):
        print(f"{file_name} is a file.")
        if tarfile.is_tarfile(file_name):
            print(f"{file_name} is a tar file.")
            return "tar"
        return [file_name]
    else:
        print(f"Error: {file_name} does not exist.")
        print(f"Hint: Current working directory: {os.getcwd()}")
        return None


def parse_log_file(file_path):
    log_entries = []

    try:
        with open(file_path, "r") as log_file:
            for line in log_file:
                log_entry = LogEntry.from_log_line(line)
                if log_entry:
                    log_entries.append(log_entry)
                else:
                    print(f"Error parsing line: {line}")
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

    return log_entries


FILES_DIR = os.path.dirname(__file__)


def get_path(filename: str) -> str:
    return os.path.join(FILES_DIR, filename)


def process_logs(path, extract_to="extracted_logs"):
    path = get_path(path)
    files_to_process = check_dir_or_file(path)

    if not files_to_process:
        print(f"Error: {path} does not exist or contains no valid files.")
        return []

    if files_to_process == "tar":
        print(f"Extracting tar file: {path}")
        files_to_process = untar_file(path, extract_to=extract_to)
        if isinstance(files_to_process, str):
            print(files_to_process)
            return []

    all_log_entries = []

    for file_path in files_to_process:
        print(f"Processing file: {file_path}")
        log_entries = parse_log_file(file_path)
        all_log_entries.extend(log_entries)

    return all_log_entries


def open_file(file_name):
    ip_counter = Counter()
    try:
        with open(file_name, "r") as log_file:
            for line in log_file:
                ip = line.split()[0]
                ip_counter[ip] += 1
    except Exception as e:
        print(f"Error reading log file: {e}")
        return []

    return ip_counter.most_common(3)


def get_top_ips(log_entries, top_n=3):
    ips = [entry.ip for entry in log_entries]

    ip_counter = Counter(ips)
    top_ips = ip_counter.most_common(top_n)
    top_ips_dict = dict(top_ips)
    return top_ips_dict


def get_total_requests(log_entries):
    return len(log_entries)


def get_top_long_requests(log_entries, top_n=3):
    top_longest_requests_sorted = sorted(
        log_entries, key=lambda x: x.time, reverse=True
    )

    top_longest_requests_sorted = top_longest_requests_sorted[:top_n]

    return [
        {
            "ip": entry.ip,
            "date": entry.date,
            "method": entry.method,
            "url": entry.url,
            "duration": entry.time,
        }
        for entry in top_longest_requests_sorted
    ]


def calculate_method_counts(log_entries):
    method_counts = defaultdict(int)

    for entry in log_entries:
        method = entry.method
        method_counts[method] += 1

    return method_counts


def accumulate_result(log_entries) -> list:
    result_list = {
        "top_ips": get_top_ips(log_entries),
        "top_longest": get_top_long_requests(log_entries),
        "total_stats": calculate_method_counts(log_entries),
        "total_requests": get_total_requests(log_entries),
    }
    return result_list


def write_result_to_json(result_list: list, output_file: str = "result.json"):
    with open(output_file, "a") as f:
        json.dump(result_list, f, indent=4)


def process_and_save_log(path):
    parsed_entries = process_logs(path)

    if not parsed_entries:
        print(f"No valid log entries found in {path}.")
        return

    result = accumulate_result(parsed_entries)

    log_file_name = os.path.basename(path)
    output_file = f"{log_file_name}_result.json"
    write_result_to_json(result, output_file)

    print(f"Statistics for {log_file_name}:")
    print(json.dumps(result, indent=4))


def main():
    parser = argparse.ArgumentParser(description="Parse and analyze log files.")

    parser.add_argument(
        "-t", "--tarfile", type=str, help="Path to the tar file", required=True
    )

    args = parser.parse_args()

    log_file = args.tarfile

    process_and_save_log(log_file)


if __name__ == "__main__":
    main()
