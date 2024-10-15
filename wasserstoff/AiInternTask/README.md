# AiInternTask

## Project Overview

The aim of this project is to parse performance logs, extract relevant metrics (such as extraction time, summary time, keyword extraction time, MongoDB insertion time, and memory usage), and generate reports in JSON and CSV formats. The project is designed to handle logs created during PDF processing, organize the data, and provide a clear view of the system's performance.

It also includes unit tests and optional Docker setup for easy deployment.

## Features

- **Log Parsing:** Parses logs to extract performance metrics.
- **Report Generation:** Generates reports in JSON and CSV formats.
- **MongoDB Integration:** Handles insertion of data into MongoDB.
- **Keyword Extraction:** Extracts keywords from PDF content.
- **Unit Testing:** Unit tests included to validate functionality.
- **Docker Setup (Optional):** Includes a Dockerfile for simplified deployment.
- **Performance Reporting:** Reports on concurrency, speed, and resource utilization.

## Project Structure

```bash
AiInternTask/
?
??? src/                       # Source code
?   ??? performance_report.py   # Script for parsing logs and generating reports
?   ??? keyword_extractor.py    # Keyword extraction logic
?   ??? mongodb_handler.py      # MongoDB insertion handler functions
?   ??? pipeline.log            # Example log file for testing
?
??? tests/                     # Unit tests
?   ??? test_keyword_extraction.py  # Test cases for keyword extraction
?   ??? test_summarization.py       # Test cases for summarization
?
??? Dockerfile                 # Docker setup file (Optional)
??? README.md                  # Project documentation
??? requirements.txt           # List of required packages
??? performance_report.py      # Evaluating the time and data


Ensure you have the following installed:

- Python 3.7 or higher
- MongoDB (for storing data)
- [Vercel](https://vercel.com) or other hosting platforms for public hosting (Optional)

### Python Libraries

Install the required Python packages using:

```bash
pip install -r requirements.txt

```bash
python -m unittest discover tests  # This will run both test_keyword_extraction.py and 
                                    test_summarization.py under the tests/ folder to validate 
                                    keyword extraction and summarization functionality.


