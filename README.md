# Multi-Agent CV Flow

This project demonstrates a sequential multi-agent workflow for CV processing and job recommendation using Python, LangChain, and LangGraph.

The system validates uploaded CV files, extracts candidate information, matches the profile against an internal job database, assesses the quality of the match, and presents recommendations. A final human-in-the-loop (HITL) step allows the user to choose whether to be contacted personally.

---

## Features

- Security validation of uploaded CV files
- Support for `.pdf` and `.docx`
- Sequential multi-agent workflow implemented with LangGraph
- Shared state passed between all agents
- 4 agents:
  1. Intake + Profiling Agent
  2. Job Matching Agent
  3. Assessment Agent
  4. Recommendation Agent
- Mocked internal job database using local JSON
- Stubbed web search for labor market context and education suggestions
- Human-in-the-loop (HITL) step via terminal after the final result

---

## Project Structure

```
multi-agent-cv-flow/
├─ pyproject.toml
├─ README.md
├─ data/
│  ├─ cv_test.docx
│  ├─ cv_test_spam.pdf
│  └─ jobs.json
└─ src/
   └─ mlops_multiagent/
      ├─ __init__.py
      ├─ main.py
      ├─ graph.py
      ├─ config.py
      ├─ state.py
      ├─ models.py
      ├─ agents/
      │  ├─ __init__.py
      │  ├─ common.py
      │  ├─ intake_profile.py
      │  ├─ job_matcher.py
      │  ├─ assessment.py
      │  └─ recommendation.py
      └─ utils/
         ├─ __init__.py
         ├─ document_loader.py
         ├─ security.py
         └─ text_processing.py
```
---

## Installation

This project uses `uv` for dependency management.

Install dependencies:

```bash
uv sync
```

---

## Running the Application

Start the program:

```bash
uv run mlops-multiagent
```

Example with arguments:

uv run mlops-multiagent \
  --cv-path ./data/cv_test.docx \
  --location Stockholm \
  --employment-type deltid \
  --language svenska \
  --driving-license ja \
  --commute-willingness nej

---

## User Input

- CV file path (.pdf or .docx)
- Job location
- Employment type (heltid/deltid)
- Optional: language, driving license, commuting willingness

---

## Output

- Job recommendations
- Skill gap analysis
- Training suggestions (if needed)
- HITL prompt (contact yes/no)

---

## Test Data

- cv_test.docx – valid CV
- cv_test_spam.pdf – should be blocked
- jobs.json – internal job database

---

## Architecture

Security -> Agent1 -> Agent2 -> Agent3 -> Agent4 -> HITL

Shared state is passed through all steps.

---

## Notes

- Educational project
- Rule-based agents
- Easy to extend with LLMs
- Internal job data only
- Stubbed web search
