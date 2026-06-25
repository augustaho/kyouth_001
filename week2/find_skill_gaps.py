import re
import sqlite3
import time
from pathlib import Path

from pydantic import BaseModel


# Required output format from the guide
class SkillGapResult(BaseModel):
    gaps: list[str]
    time: int = 0
    tokens: int = 0


# Placeholder from Day 1-2 should not be treated as a skill
PLACEHOLDER = "no tech stack extracted"


def clean_skill(skill: str) -> str:
    """Convert skill to lowercase and remove extra spaces."""

    return skill.strip().lower()


def split_skills(text: str) -> list[str]:
    """Split comma-separated skills into a clean skill list."""

    if not text:
        return []

    if text.strip().lower() == PLACEHOLDER:
        return []

    # Protect skills that should NOT be split by /
    text = text.replace("A/B Testing", "AB_TESTING")
    text = text.replace("A/B testing", "AB_TESTING")
    text = text.replace("a/b testing", "AB_TESTING")
    text = text.replace("CI/CD", "CICD")
    text = text.replace("ci/cd", "CICD")

    skills = []

    # First split by comma
    for item in text.split(","):
        item = item.strip()

        # Then split slash skills like AWS/Azure/GCP
        for part in item.split("/"):
            part = part.strip()

            # Restore protected skills
            part = part.replace("AB_TESTING", "A/B Testing")
            part = part.replace("CICD", "CI/CD")

            skill = clean_skill(part)

            if skill:
                skills.append(skill)

    return skills


def extract_resume_skills(resume_text: str) -> set[str]:
    """Extract only the Technical Skills section from resume."""

    # Find text between "Technical Skills:" and "Languages:"
    match = re.search(
        r"technical skills\s*:\s*(.*?)(languages\s*:|additional skills\s*:|certifications\s*:|$)",
        resume_text,
        re.IGNORECASE | re.DOTALL,
    )

    if not match:
        return set()

    skills_text = match.group(1)

    return set(split_skills(skills_text))


def read_job_skills(db_url: str) -> set[str]:
    """Read all tech_stack values from jobs table."""

    conn = sqlite3.connect(db_url)
    cursor = conn.cursor()

    cursor.execute("SELECT tech_stack FROM jobs")
    rows = cursor.fetchall()

    conn.close()

    job_skills = set()

    for row in rows:
        tech_stack = row[0]

        for skill in split_skills(tech_stack):
            job_skills.add(skill)

    return job_skills


def estimate_tokens(resume_text: str, job_skills: set[str], gaps: list[str]) -> int:
    """Estimate tokens using 4 tokens per word."""

    text = resume_text + " " + " ".join(job_skills) + " " + " ".join(gaps)

    return len(text.split()) * 4


def find_skill_gaps(input_file_path: str, db_url: str) -> SkillGapResult:
    """Find skills required by jobs but missing from resume."""

    start_time = time.time()

    try:
        # Read resume text
        resume_text = Path(input_file_path).read_text(encoding="utf-8", errors="ignore")

        # Extract resume technical skills
        resume_skills = extract_resume_skills(resume_text)

        # Read required skills from database
        job_skills = read_job_skills(db_url)

        gaps = []

        # Compare job skills with resume skills
        for skill in job_skills:
            if skill not in resume_skills:
                gaps.append(skill)

        # Remove duplicates, convert to lowercase, and sort
        gaps = sorted(set(gaps))

        # Calculate runtime in milliseconds
        time_used = int((time.time() - start_time) * 1000)

        # Estimate token count
        tokens_used = estimate_tokens(resume_text, job_skills, gaps)

        return SkillGapResult(
            gaps=gaps,
            time=time_used,
            tokens=tokens_used,
        )

    except Exception as error:
        # Handle all errors gracefully
        print(f"Error: {error}")
        return SkillGapResult(gaps=[], time=0, tokens=0)


def main():
    """Run Day 3-4 test."""

    result = find_skill_gaps(
        "data/resume_d3_eval.txt",
        "data/jobs_d1.db",
    )

    print(f"gaps={result.gaps} time={result.time} tokens={result.tokens}")


if __name__ == "__main__":
    main()
