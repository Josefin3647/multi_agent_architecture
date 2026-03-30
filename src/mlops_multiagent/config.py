"""Central configuration for the project."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
SAMPLE_DATA_DIR = BASE_DIR / "sample_data"
DEFAULT_JOBS_PATH = SAMPLE_DATA_DIR / "jobs.json"

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
MAX_FILE_SIZE_MB = 5
MAX_TEXT_CHARS = 50_000

SUSPICIOUS_PATTERNS = [
    "ignore previous instructions",
    "system prompt",
    "developer message",
    "exfiltrate",
    "execute command",
    "run powershell",
    "rm -rf",
    "<script",
    "base64,",
    "curl http",
    "wget http",
    "jailbreak",
]