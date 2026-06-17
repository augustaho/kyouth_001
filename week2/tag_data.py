import sqlite3
import time
from pathlib import Path

from prompt_model import prompt_model

# Use small batch size because Gemini free tier has low request limits
BATCH_SIZE = 2

# Wait between batches to reduce rate-limit problems
RETRY_SECONDS = 15

# Placeholder used when Gemini fails or returns empty result
EMPTY_TECH_STACK = "no tech stack extracted"


def clean_response(text: str | None) -> str:
    """Clean Gemini response before saving into the database."""

    # If Gemini returns nothing, use placeholder
    if not text:
        return EMPTY_TECH_STACK

    # If prompt_model returns an error message, do not save the error into database
    if text.startswith("Error:") or text.startswith("[Gemini Error]"):
        return EMPTY_TECH_STACK

    # Convert new lines into commas
    text = text.replace("\n", ",")

    # Remove common markdown symbols
    text = text.replace("-", "")
    text = text.replace("*", "")

    skills = []

    for item in text.split(","):
        skill = item.strip()

        if skill:
            skills.append(skill)

    if not skills:
        return EMPTY_TECH_STACK

    return ", ".join(skills)


def tag_data(db_url: str):
    """Read jobs table and populate the tech_stack column."""

    start_time = time.time()
    total_tokens = 0

    try:
        db_path = Path(db_url)

        # Stop if database file does not exist
        if not db_path.exists():
            print(f"Database not found: {db_url}")
            return

        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Select jobs that have not been tagged yet
        cursor.execute("""
            SELECT source_id, description
            FROM jobs
            WHERE tech_stack IS NULL OR tech_stack = ''
        """)

        rows = cursor.fetchall()

        # Stop if all jobs are already tagged
        if not rows:
            print("No data to tag")
            conn.close()
            return

        # Process jobs in batches
        for i in range(0, len(rows), BATCH_SIZE):
            batch = rows[i:i + BATCH_SIZE]

            updates = []

            for source_id, description in batch:
                prompt = f"""
Extract the technical stack used in this job description.

Rules:
- Return comma separated values only.
- Include programming languages, frameworks, databases, cloud tools, and technical tools.
- Ignore non-technical soft skills like leadership and management.
- Ignore certifications.
- Do not include explanation.

Job description:
{description}
"""

                try:
                    # Send prompt to Gemini
                    response = prompt_model("gemini-2.5-flash", prompt)

                    # Clean Gemini output
                    tech_stack = clean_response(response)

                    # Estimate token count using 4 tokens per word
                    total_tokens += (len(prompt.split()) + len(str(response).split())) * 4

                except Exception as error:
                    # Do not crash if Gemini/API fails
                    tech_stack = EMPTY_TECH_STACK
                    print(f"Failed to analyze Job {source_id}: {error}")

                # Store update for batch writing
                updates.append((tech_stack, source_id))

                # Print result as required by guide
                print(f"Analyzed Job {source_id}: {tech_stack}")

            # Write current batch into database
            cursor.executemany("""
                UPDATE jobs
                SET tech_stack = ?
                WHERE source_id = ?
            """, updates)

            conn.commit()

            # Wait before next batch
            time.sleep(RETRY_SECONDS)

        total_time = round((time.time() - start_time) * 1000, 2)

        print(f"Total tokens used: {total_tokens}, took {total_time}ms")

        conn.close()

    except Exception as error:
        # Catch unexpected errors gracefully
        print(f"Unexpected error: {error}")


# Run this file directly for testing
if __name__ == "__main__":
    tag_data("data/jobs_d1.db")