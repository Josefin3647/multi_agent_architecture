# Multi-Agent CV Flow

Ett pedagogiskt exempel på ett sekventiellt multi-agent-flöde byggt med Python, LangChain och LangGraph.

## Funktioner

- Säkerhetskontroll av inkommande CV-fil
- Stöd för `.pdf` och `.docx`
- 4 agenter:
  1. Intake + Profilagent
  2. Jobbmatchningsagent
  3. Bedömningsagent
  4. Rekommendationsagent
- Mockad intern jobbdatakälla via lokal JSON
- Stubbad webbsökning för kompetens- och utbildningsförslag
- HITL-steg i terminalen

## Projektstruktur

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

## Testdata

Mappen `sample_data/` innehåller filer för att testa flödet:

- `cv_test.docx` – exempel på ett giltigt CV som går igenom hela flödet
- `cv_test_spam.pdf` – innehåller avsiktligt misstänkt innehåll och ska stoppas i säkerhetskontrollen
- `jobs.json` – mockad intern jobbdatakälla som används för matchning

### Testa flödet

**Godkänt flöde:**
1. Kör programmet
2. Ange `sample_data/cv_test.docx`
3. Fyll i uppgifterna
4. Verifiera att alla agenter körs och att du får en rekommendation + HITL-fråga

**Säkerhetskontroll:**
1. Kör programmet
2. Ange `sample_data/cv_test_spam.pdf`
3. Verifiera att flödet stoppas före Agent 1