# 3_gold/loader.py
# JSON to SQLite database
import os
import json
import sqlite3


def load_all_jsons(input_dir, db_path):

    # Create gold folder if it does not exist
    os.makedirs(
        os.path.dirname(db_path),
        exist_ok=True,
    )

    # Connect to SQLite database
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Create a table named jobs
    # Ensure unique source_id to prevent duplicates
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            source_id TEXT PRIMARY KEY, 
            job_title TEXT,
            company TEXT,
            description TEXT
        )
    """)

    total = 0
    inserted = 0
    skipped = 0

    print("🥇 Gold:")

    # Read every JSON file from silver folder
    for filename in os.listdir(input_dir):
        if filename.endswith(".json"):
            total += 1
            file_path = os.path.join(input_dir, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            # Avoid crashing if error occurs during insertion, and log the error
            try:
                cursor.execute("""
                    INSERT OR IGNORE INTO jobs 
                    (source_id, job_title, company, description)
                    VALUES (?, ?, ?, ?)
                """, (
                    data.get("source_id"),
                    data.get("job_title"),
                    data.get("company"),
                    data.get("description"),
                ))

                inserted += 1
                print(f"✅ Inserted: {filename}")

            # If source_id already exists, skip and log a warning
            except sqlite3.IntegrityError:
                skipped += 1
                print(f"⏭️ Skipped (duplicate): {filename}")

    # Commit changes and close connection
    connection.commit()
    connection.close()

    print("\n📊 Gold Summary:")
    print(f"Total: {total} | Inserted: {inserted} | Skipped: {skipped}")