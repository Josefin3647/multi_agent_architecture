from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class UserInput:
    cv_path: str
    location: str
    employment_type: str
    language: str | None = None
    driving_license: bool | None = None
    commute_willingness: bool | None = None