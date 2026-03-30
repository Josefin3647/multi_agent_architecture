from __future__ import annotations

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data"
JOBS_FILE = DATA_DIR / "jobs.json"

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE_BYTES = 5 * 1024 * 1024  # 5 MB

SUSPICIOUS_PATTERNS = [
    r"ignore previous instructions",
    r"system prompt",
    r"developer message",
    r"do not follow",
    r"<script",
    r"javascript:",
    r"powershell",
    r"cmd\.exe",
    r"base64",
    r"wget\s+http",
    r"curl\s+http",
]