import sys
from pathlib import Path


from ingestor import ingest_all_mhtml
from processor import process_all_html
from loader import load_all_jsons
from profiler import run_data_profile

# Main entry point of the program
def main():

    # Check whether user provided a command
    if len(sys.argv) < 2:
        print("Insert command: python main.py [ingest OR process OR load OR profile OR all]")
        return

    command = sys.argv[1]

    # Day 1: Run Bronze Layer ingestion
    if command == "ingest":

        input_dir = Path("data/0_source")
        output_dir = Path("data/1_bronze")

        ingest_all_mhtml(
            input_dir,
            output_dir,
        )

    # Day 2: Run Silver Layer processing
    elif command == "process":
        input_dir = Path("data/1_bronze")
        output_dir = Path("data/2_silver")

        process_all_html(input_dir, output_dir)

    # Day 3: Run Gold Layer loading
    elif command == "load":
        load_all_jsons()
    
    # Day 4: Run Data Profiling
    elif command == "profile":
        db_path = Path("data/3_gold/jobs.db")
        run_data_profile(db_path)

    # All
    elif command == "all":
        ingest_all_mhtml(Path("data/0_source"), Path("data/1_bronze"))
        process_all_html(Path("data/1_bronze"), Path("data/2_silver"))
        load_all_jsons()
        run_data_profile(Path("data/3_gold/jobs.db"))

    else:
        print(
            f"Unknown command: {command}"
        )


# Start program execution
if __name__ == "__main__":
    main()
