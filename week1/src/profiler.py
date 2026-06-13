# 4/profiler.py
# Data quality profiling
import sqlite3
import os


def run_data_profile(db_path):
    # If database does not exist, do not crash
    if not os.path.exists(db_path):
        print(f"❌ Database not found at {db_path}")
        return

    # Connect to SQLite database and run queries to get data quality metrics
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Count total records
    cursor.execute("SELECT COUNT(*) FROM jobs")
    total_records = cursor.fetchone()[0] #Retrieve result of query

    # Count missing values for each field
    cursor.execute("""
        SELECT 
            SUM(CASE WHEN job_title IS NULL OR job_title = '' THEN 1 ELSE 0 END),
            SUM(CASE WHEN company IS NULL OR company = '' THEN 1 ELSE 0 END),
            SUM(CASE WHEN description IS NULL OR description = '' THEN 1 ELSE 0 END)
        FROM jobs
    """)
    missing_job_title, missing_company, missing_description = cursor.fetchone()

    # Average description length
    cursor.execute("SELECT AVG(LENGTH(description)) FROM jobs")
    avg_description_length = cursor.fetchone()[0]

    # Shortest description
    # Limit 1 only take the first
    cursor.execute("""
        SELECT source_id, job_title, LENGTH(description)
        FROM jobs
        ORDER BY LENGTH(description) ASC
        LIMIT 1 
    """)
    shortest = cursor.fetchone()

    # Longest description
    cursor.execute("""
        SELECT source_id, job_title, LENGTH(description)
        FROM jobs
        ORDER BY LENGTH(description) DESC
        LIMIT 1 
    """)
    longest = cursor.fetchone()

    print("\n--- 🔍 DATA QUALITY REPORT ---")
    print(f"📈 Total Records: {total_records}")
    print(f"❓ Missing Values -> job_title: {missing_job_title}, company: {missing_company}, description: {missing_description}")
    print(f"📝 Avg Description Length: {int(avg_description_length)} chars")

    print(f"⚠️  Shortest Description: {shortest[2]} chars")
    print(f" ↳ source_id: {shortest[0]} | job_title: {shortest[1]}")

    print(f"🚨 Longest Description: {longest[2]} chars")
    print(f" ↳ source_id: {longest[0]} | job_title: {longest[1]}")

    conn.close()