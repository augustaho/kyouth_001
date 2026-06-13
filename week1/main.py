import sys
from pathlib import Path


from src.ingestor import ingest_all_mhtml
from src.processor import process_all_html
from src.loader import load_all_jsons
from src.profiler import run_data_profile

# Main entry point of the program
def main():

    # Check whether user provided a command
    if len(sys.argv) < 2:
        print("Insert command: python main.py [ingest OR process OR load OR profile OR all]")
        return

    command = sys.argv[1]

    source_dir = Path("data/0_source")
    bronze_dir = Path("data/1_bronze")
    silver_dir = Path("data/2_silver")
    gold_dir = Path("data/3_gold")
    db_path = gold_dir / "jobs.db"

    # Day 1: Run Bronze Layer ingestion
    if command == "ingest":
        ingest_all_mhtml(source_dir, bronze_dir)

    # Day 2: Run Silver Layer processing
    elif command == "process":
        process_all_html(bronze_dir, silver_dir)

    # Day 3: Run Gold Layer loading
    elif command == "load":
        load_all_jsons(silver_dir, db_path)
    
    # Day 4: Run Data Profiling
    elif command == "profile":
        run_data_profile(db_path)

    # All
    elif command == "all":
        ingest_all_mhtml(source_dir, bronze_dir)
        process_all_html(bronze_dir, silver_dir)
        load_all_jsons(silver_dir, db_path)
        run_data_profile(db_path)

    else:
        print(
            f"Unknown command: {command}"
        )


# Start program execution
if __name__ == "__main__":
    main()
