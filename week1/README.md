# kyouth_001

# Job Data Pipeline

## Project Description

This projects build an ETL (Extract, Transform, Load) pipeline for jobs.db database, which follows a Medallion Architecture (A data design pattern used to logically organize data in a lakehouse, with the goal of incrementally and progressively improving the structure and quality of data.).
The process is broken down into the following:
    1. Bronze- Data Ingestion: Read raw MHTML files and convert them into HTML files
    2. Silver- Data Cleaning & Processing, Structuring: Extract job information and saved as JSON files.
    3. Gold- Data Storage & Idempotent Loading: Store data in SQLite Database, Prevent duplication.
    4. Data Profiling & Ochestration: Run quality check of database, Use main.py to run each step or full pipeline.


## Setup Instructions
Before running the project, ensure the following are installed:
    - python version 3.14
    - Git

Clone Repository using:
    git clone https://github.com/augustaho/kyouth_001.git

Install Dependencies Required:
    pip install beautifulsoup4
    pip install pydantic


## Usage

To run the program, Insert command in the terminal: python main.py [ingest OR process OR load OR profile OR all]. (e.g. python main.py ingest)


## Technical Reflections

Day 1: The Extractor (Medallion & Lakehouses)

Question: Why is it useful to keep the original raw HTML files instead of directly inserting processed data into the database? What problems become easier to debug or recover from?

Answer: Keeping original file makes troubleshooting easier. When error occurs during extraction, the processing step can be rerun using the existing files instead of collecting the data again.


Day 2: Treatment Plant (ETL vs ELT & Scale)

Question: Why do cloud systems prefer loading raw data first before cleaning it (ELT)? What problems happen when processing files sequentially, and how does distributed processing help?

Answer: Cloud systems prefer loading raw data first as it acts as a backup. If the cleaning logic changes later, the raw data can be processed again without needing to recollect the data again. 
The system will become slow when amount of data grows which will delay the entire pipeline. Distributed processing helps by processing multiple files parallely across different machines, allowing large datasets to be handled more efficiently.