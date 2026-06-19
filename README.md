# Week 2: AI Component - Resume Skill Gap Analyzer

## Project Overview

This project builds the AI component of a Resume Skill Gap Analyzer. The system reads job descriptions from a SQLite database, extracts required technical skills into a `tech_stack` column, then compares those job-required skills with skills found in a resume. The final output is a sorted lowercase list of missing skills, also known as skill gaps.

## Setup Instructions

Prerequisites:

* Python 3.14.*
* uv
* Git
* Gemini API key
* Ollama 0.21.* installed for setup requirement

Install dependencies:

```bash
uv sync
```

Create a `.env` file:

```env
GOOGLE_API_KEY=your_api_key_here
```

Do not commit `.env` to GitHub.

## Usage

Run Gemini prompt test:

```bash
uv run python main.py gemini-2.5-flash "tell me one malaysian joke"
```

Run Day 1-2 tagging:

```bash
uv run python tag_data.py
```

Expected output:

```text
Analyzed Job 91397216: Python, SQL, Java, ...
No data to tag
```

Run Day 3-4 skill gap detection:

```bash
uv run python find_skill_gaps.py
```

Expected output:

```text
gaps=['alibaba cloud', 'api integration', 'aws', ...] time=1 tokens=976
```

## API / Function Reference

### `prompt_model(model: str, prompt: str) -> str`

Sends a prompt to Gemini and returns the model response as text. It loads the API key from `.env` and handles errors gracefully.

### `tag_data(db_url: str)`

Reads the `jobs` table from SQLite, finds rows with empty `tech_stack`, sends job descriptions to Gemini, extracts technical skills, and updates the database. It uses batch processing and a retry delay to reduce rate-limit issues.

### `find_skill_gaps(input_file_path: str, db_url: str) -> SkillGapResult`

Reads a resume text file and a tagged jobs database. It compares resume skills with job-required skills and returns missing skills as a Pydantic model.

```python
class SkillGapResult(BaseModel):
    gaps: list[str]
    time: int = 0
    tokens: int = 0
```

## Data / Assumptions

The system uses:

* `jobs_d1.db` for Day 1-2 tagging
* `jobs_d3_eval.db` for Day 3-4 evaluation
* `resume_d3.txt` or `resume_d3_eval.txt` as resume input
* `d3_truth.json` for validation

The `jobs` table is expected to contain:

* `source_id`
* `job_title`
* `company`
* `description`
* `tech_stack`

Assumptions:

* Job descriptions are stored in the `description` column.
* Extracted skills are stored as comma-separated text in `tech_stack`.
* Resume input is already converted into plain text.
* Non-technical skills such as cooking, leadership, and management are ignored.
* `A/B testing` and `CI/CD` are not split by `/`.
* Skills such as `AWS/Azure/GCP` are split into separate skills.

## Testing

The system was tested using the provided sample databases and resume files.

Testing performed:

* Ran `tag_data.py` on `jobs_d1.db`.
* Confirmed each job received a `tech_stack` value.
* Reran `tag_data.py` and confirmed it printed `No data to tag`.
* Ran `find_skill_gaps.py` on `resume_d3_eval.txt` and `jobs_d3_eval.db`.
* Compared the output with `d3_truth.json`.
* Confirmed the result matched the expected answer.

## Limitations

* Gemini responses may occasionally fail due to API issues such as `503 UNAVAILABLE`.
* LLM-based tagging may produce slightly different skills across runs.
* Empty or failed extraction is stored as `no tech stack extracted`.
* Skill matching is mostly text-based, so semantic equivalents may not always be detected.
* The system focuses on technical skills and intentionally ignores certifications and soft skills.
* MCP integration and advanced optimization are not included in the mandatory version.

## Architecture Reflection

I separated the project into different files to keep each part easier to understand. `prompt_model.py` handles model communication, `tag_data.py` handles job skill extraction, and `find_skill_gaps.py` handles deterministic skill gap comparison.

For Day 1-2, I used Gemini because it is faster and easier to run than local models. I used small batch sizes and retry delays to reduce rate-limit issues. For Day 3-4, I used deterministic Python matching instead of asking the LLM to decide the final gaps because the guide requires consistent results across runs.

The main trade-off is simplicity versus advanced accuracy. This version is easier to explain and debug, but it may not detect every possible synonym or related skill. Given more time, I would improve skill normalization, add quality metrics, and explore MCP integration.
