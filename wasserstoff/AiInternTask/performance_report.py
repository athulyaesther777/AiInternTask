import re
import json
import pandas as pd
import os

def parse_log(log_file):
    performance_data = []
    # Regex pattern to capture the performance metrics from the log file
    performance_pattern = r"Performance metrics for (.+): {'extraction_time': (.+), 'summary_time': (.+), 'keyword_extraction_time': (.+), 'mongodb_insertion_time': (.+), 'memory_usage': (.+)}"

    with open(log_file, 'r') as file:
        for line in file:
            # Print each line for debugging purposes (optional)
            print(f"Parsing line: {line.strip()}")
            match = re.search(performance_pattern, line)
            if match:
                document_name = match.group(1)
                extraction_time = float(match.group(2))
                summary_time = float(match.group(3))
                keyword_extraction_time = float(match.group(4))
                mongodb_insertion_time = float(match.group(5))
                memory_usage = int(match.group(6))

                # Append the extracted performance data into the list
                performance_data.append({
                    "document": document_name,
                    "extraction_time": extraction_time,
                    "summary_time": summary_time,
                    "keyword_extraction_time": keyword_extraction_time,
                    "mongodb_insertion_time": mongodb_insertion_time,
                    "memory_usage": memory_usage,
                })

    return performance_data


def save_report(performance_data, output_file):
    # Save performance data to a JSON file
    with open(output_file, 'w') as json_file:
        json.dump(performance_data, json_file, indent=4)

    # Optionally, save the performance data to a CSV file
    df = pd.DataFrame(performance_data)
    df.to_csv(output_file.replace('.json', '.csv'), index=False)

if __name__ == "__main__":
    # Correct path to the log file
    log_file = r'C:\Users\91730\pythonProject\pdfsummarizer\pythonProject1\src\pipeline.log'

    # Check if the log file exists
    if not os.path.exists(log_file):
        print(f"Log file not found at {log_file}. Please check the path.")
    else:
        # Parse the log file and extract performance data
        performance_data = parse_log(log_file)

        # Save the performance data to a report
        save_report(performance_data, 'performance_report.json')
        print("Performance report generated successfully.")
