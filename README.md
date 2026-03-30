# Multi-Agent CV Flow

A pedagogical example of a sequential multi-agent workflow built with Python, LangChain, and LangGraph.

## Features

- Security validation of uploaded CV files
- Support for `.pdf` and `.docx`
- 4 agents:
  1. Intake + Profiling Agent
  2. Job Matching Agent
  3. Assessment Agent
  4. Recommendation Agent
- Mocked internal job database using local JSON
- Stubbed web search for skills and education suggestions
- Human-in-the-loop (HITL) step via terminal

## Project Structure

```text
multi-agent-cv-flow/
├─ pyproject.toml
├─ README.md
├─ sample_data/
│  ├─ jobs.json
│  └─ example_cv.txt
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

## Installation

This project uses uv for dependency management.

Install dependencies:

```bash
uv sync
```

## Running the Application

Start the program:

```bash
uv run mlops-multiagent
```

Follow the instructions in the terminal:

- Provide the path to your CV file (.pdf or .docx)
- Enter preferred job location
- Choose employment type (full-time/part-time)
- Optionally provide languages, driver's license, and commuting preference

After processing, you will receive:

- Job recommendations
- Skill gap analysis (if applicable)
- A HITL prompt asking if you want to be contacted

## Test Data

The sample_data/ folder contains files for testing the workflow:

- cv_test.docx – example of a valid CV that passes through the full pipeline
- cv_test_spam.pdf – contains intentionally suspicious content and should be blocked by the security check
- jobs.json – mocked internal job database used for matching

## Testing the Flow
Valid Flow
Run the program
Provide sample_data/cv_test.docx
Fill in the requested inputs
Verify that all agents execute and produce a final recommendation + HITL prompt

## Security Validation
Run the program
Provide sample_data/cv_test_spam.pdf
Verify that the workflow is stopped before Agent 1

## How It Works

The system is built as a sequential multi-agent workflow using LangGraph:

Security Check
Validates file type, size, and content
Stops the flow if suspicious patterns are detected´

Agent 1 – Intake & Profiling
Extracts experience, skills, and education from the CV
Builds a structured candidate profile
Agent 2 – Job Matching
Matches the profile against a local job database
Scores and ranks relevant job postings
Agent 3 – Assessment
Evaluates match quality
Identifies skill gaps
Uses stubbed web search for additional context
Agent 4 – Recommendation
Presents job matches and/or training suggestions
Explains reasoning in a user-friendly way
HITL (Human-in-the-Loop)
User chooses whether to be contacted
Collects name and email if applicable
Notes
The implementation is intentionally simple and modular for educational purposes
Agents are rule-based but can easily be replaced with LLM-powered logic
Job matching uses internal data only (no external APIs)
Web search in Agent 3 is simulated via a stub function