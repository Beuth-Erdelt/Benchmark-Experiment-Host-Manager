
#s = "2025-01-20 09:39:58:594 100 sec: 2036253 operations; 30182.9 current ops/sec; est completion in 11 minutes [READ: Count=150931, Max=489215, Min=188, Avg=1076.26, 90=687, 99=1556, 99.9=270591, 99.99=426239] [UPDATE: Count=151507, Max=489471, Min=221, Avg=3163.81, 90=1142, 99=107967, 99.9=346623, 99.99=488703]"

import re
from datetime import datetime

def parse_string(log):
    try:
        # Extract the date and time
        date_time_match = re.match(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}:\d{3})", log)
        date_time_str = date_time_match.group(1) if date_time_match else None
        date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S:%f") if date_time_str else None
        # Extract all numbers
        #all_numbers = re.findall(r"\b\d+\.?\d*\b", log)
        # Extract metrics from sections like [READ: ...] or [UPDATE: ...]
        # Match the pattern for operations and ops/sec
        match = re.search(r"(\d+)\s+operations", log)
        if match:
            total_operations = int(match.group(1))  # First captured group
        # Match the pattern for operations and ops/sec
        match = re.search(r"(\d+)\s+sec:", log)
        if match:
            sec = int(match.group(1))  # First captured group
        # Match the pattern for operations and ops/sec
        match = re.search(r";\s+([\d.]+)\s+current ops/sec", log)
        if match:
            current_ops_per_sec = float(match.group(1))  # First captured group
        sections = re.findall(r"\[(\w+): ([^\]]+)\]", log)
        metrics = {}
        for section, content in sections:
            # Extract key-value pairs
            metrics[section] = {}
            for key_value in content.split(", "):
                key, value = key_value.split("=")
                metrics[section][key] = float(value) if "." in value else int(value)
        return {
            "date_time": date_time,
            "sec": sec,
            "total_operations": total_operations,
            "current_ops_per_sec": current_ops_per_sec,
            #"all_numbers": list(map(float, all_numbers)),  # Convert all numbers to float
            "metrics": metrics,
        }
    except Exception as e:
        # Log or handle any parsing errors (optional)
        return None

# Example string
log_str = """2025-01-20 09:39:58:594 100 sec: 2036253 operations; 30182.9 current ops/sec; est completion in 11 minutes [READ: Count=150931, Max=489215, Min=188, Avg=1076.26, 90=687, 99=1556, 99.9=270591, 99.99=426239] [UPDATE: Count=151507, Max=489471, Min=221, Avg=3163.81, 90=1142, 99=107967, 99.9=346623, 99.99=488703]"""

# Parse the log string
parsed_data = parse_string(log_str)

# Output
print(parsed_data)


def parse_file(file_path):
    results = []
    with open(file_path, 'r') as file:
        for line in file:
            parsed_data = parse_string(line.strip())
            if parsed_data:
                results.append(parsed_data)
    return results

# Example usage
file_path = '/home/perdelt/benchmarks/1737365651/bexhoma-benchmarker-postgresql-64-8-196608-1737365651-1-1-tgwps.dbmsbenchmarker.log'  # Replace with the path to your log file
parsed_results = parse_file(file_path)

# Output results
for result in parsed_results:
    print(result)

