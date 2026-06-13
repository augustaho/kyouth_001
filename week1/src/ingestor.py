# 1_bronze/ingestor.py  
# MHTML to HTML
from email import policy # Handle email-like formats, which MHTML is based on
from email.parser import BytesParser # Parse MHTML files, which are email-like format that can contain HTML content
from pathlib import Path # Manage file paths more easily
import quopri # Handle encoded content, which is common in MHTML files 


# Extract HTML content from a single MHTML file
def extract_html_from_mhtml(mhtml_path):
    # Open MHTML file in binary mode
    with mhtml_path.open("rb") as file:
        message = BytesParser(policy=policy.default).parse(file)

    # Search all parts of the MHTML file
    for part in message.walk():

        # Find the HTML section
        if part.get_content_type() == "text/html":

            # Try normal decoding first
            payload = part.get_payload(decode=True)

            # Handle quoted-printable encoded content
            if payload is None:
                payload = part.get_payload().encode(
                    "utf-8",
                    errors="ignore",
                )
                payload = quopri.decodestring(payload)

            # Convert bytes into readable text
            return payload.decode(
                "utf-8",
                errors="ignore",
            )

    # Return None if no HTML content is found
    return None


# Process all MHTML files from source folder
def ingest_all_mhtml(input_dir, output_dir):
    input_path = Path(input_dir)
    output_path = Path(output_dir)

    # Create bronze folder if it does not exist
    output_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Handle missing source folder
    if not input_path.exists():
        print(f"⚠️ Source directory not found: {input_path}")
        print("Bronze Summary:")
        print("Total: 0 | Extracted: 0 | Failed: 0")
        return

    # Get all MHTML files
    files = sorted(input_path.glob("*.mhtml"))

    total = len(files)
    extracted = 0
    failed = 0

    print("🥉 Bronze:...")

    # Process files one by one
    for file_path in files:

        html = extract_html_from_mhtml(file_path)

        if html:

            # Create output filename with .html extension
            output_file = (
                output_path /
                f"{file_path.stem}.html"
            )

            # Save extracted HTML
            output_file.write_text(
                html,
                encoding="utf-8",
            )

            extracted += 1
            
            print(
                f"✅ Extracted: {file_path.name}"
            )

        else:
            failed += 1
            print(
                f"⚠️ No HTML content found in: "
                f"{file_path.name}"
            )

    # Display final summary
    print()
    print("📊 Bronze Summary:")
    print(
        f" Total: {total} | "
        f" Extracted: {extracted} | "
        f" Failed: {failed}"
    )