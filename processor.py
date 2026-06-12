# 2_silver/processor.py
# HTML to JSON
import json
from pathlib import Path
from bs4 import BeautifulSoup # Undertsand and extract data from HTML files
from pydantic import BaseModel # Every job records follow same structure

# Define a Pydantic model for job listings
class JobListing(BaseModel):
    source_id: str
    job_title: str
    company: str
    description: str

# Read HTML files from bronze, extract job details, and save as JSON in silver
def process_all_html(input_dir, output_dir):
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Create silver folder if it does not exist
    output_path.mkdir(parents=True, exist_ok=True)

    # Count total HTML files, successfully processed files, and skipped files due to missing fields
    total = 0
    processed = 0
    skipped = 0


    print("🥈 Silver...")

    # Read every HTML file from bronze folder one by one
    for html_file in input_path.glob("*.html"):
        total += 1

        # Open HTML file using utf-8 encoding and parse with BeautifulSoup
        with open(html_file, "r", encoding="utf-8") as file:
            soup = BeautifulSoup(file, "html.parser")

        # Get source_id from og:url
        og_url = soup.find("meta", property="og:url")

        # If og:url is missing, skip this file and log a warning
        if og_url is None:
            print(f"⚠️  Missing og:url in: {html_file.name}")
            skipped += 1
            continue

        # Extract source_id from og:url content
        source_url = og_url.get("content", "")
        # Remove trailing slash and get last part of URL as source_id
        source_id = source_url.rstrip("/").split("/")[-1]

        # Extract required job fields
        job_title_tag = soup.find(attrs={"data-automation": "job-detail-title"})
        company_tag = soup.find(attrs={"data-automation": "advertiser-name"})
        description_tag = soup.find(attrs={"data-automation": "jobAdDetails"})

        # Check for missing fields and skip if any are missing, while logging a warning
        if job_title_tag is None:
            print(f"⚠️  Missing job_title in: {html_file.name}")
            skipped += 1
            continue

        if company_tag is None:
            print(f"⚠️  Missing company in: {html_file.name}")
            skipped += 1
            continue

        if description_tag is None:
            print(f"⚠️  Missing description in: {html_file.name}")
            skipped += 1
            continue

        # Create JobListing object and save as JSON in silver folder
        job = JobListing(
            source_id=source_id,
            job_title=job_title_tag.get_text(separator=" ", strip=True),
            company=company_tag.get_text(separator=" ", strip=True),
            description=description_tag.get_text(separator=" ", strip=True),
        )

        # Same filename as HTML but with .json extension
        output_file = output_path / f"{html_file.stem}.json"

        # Save processed job details as JSON
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(
                job.model_dump(),
                file,
                indent=4, # Make JSON human-readable with indentation
                ensure_ascii=False # Preserve non-ASCII characters in JSON (Chinese characters)
            )

        print(f"✅ Processed: {html_file.name}")
        processed += 1

    print("\n📊 Silver Summary:")
    print(f"Total: {total} | Processed: {processed} | Skipped: {skipped}")