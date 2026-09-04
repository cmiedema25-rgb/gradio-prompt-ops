"""Deterministic rubric checks for prompt-ops scoring."""

from __future__ import annotations

import json
import re
from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass
class Rubric:
    required_terms: list[str] = field(default_factory=list)
    forbidden_terms: list[str] = field(default_factory=list)
    min_chars: int = 0
    max_chars: int = 4000
    requires_json: bool = False
    requires_numbered_list: bool = False

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> Rubric:
        return cls(
            required_terms=list(raw.get("required_terms") or []),
            forbidden_terms=list(raw.get("forbidden_terms") or []),
            min_chars=int(raw.get("min_chars") or 0),
            max_chars=int(raw.get("max_chars") or 4000),
            requires_json=bool(raw.get("requires_json")),
            requires_numbered_list=bool(raw.get("requires_numbered_list")),
        )


@dataclass
class CheckResult:
    name: str
    passed: bool
    detail: str


@dataclass
class ScoreCard:
    text: str
    passed: int
    total: int
    score: float
    checks: list[CheckResult]
    all_passed: bool

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def score_text(text: str, rubric: Rubric) -> ScoreCard:
    checks: list[CheckResult] = []
    lowered = text.lower()
    for term in rubric.required_terms:
        ok = term.lower() in lowered
        checks.append(CheckResult("required", ok, f"required term {term!r}"))
    for term in rubric.forbidden_terms:
        ok = term.lower() not in lowered
        checks.append(CheckResult("forbidden", ok, f"forbidden term {term!r} absent"))
    checks.append(
        CheckResult(
            "min_chars",
            len(text) >= rubric.min_chars,
            f"len {len(text)} >= {rubric.min_chars}",
        )
    )
    checks.append(
        CheckResult(
            "max_chars",
            len(text) <= rubric.max_chars,
            f"len {len(text)} <= {rubric.max_chars}",
        )
    )
    if rubric.requires_json:
        ok = True
        detail = "valid JSON object"
        try:
            parsed = json.loads(text)
            ok = isinstance(parsed, dict)
            if not ok:
                detail = "JSON was not an object"
        except json.JSONDecodeError as exc:
            ok = False
            detail = str(exc)
        checks.append(CheckResult("json", ok, detail))
    if rubric.requires_numbered_list:
        ok = bool(re.search(r"^\s*1\.\s+", text, re.M))
        checks.append(CheckResult("numbered_list", ok, "starts a 1. item"))
    passed = sum(1 for c in checks if c.passed)
    total = len(checks)
    return ScoreCard(
        text=text,
        passed=passed,
        total=total,
        score=round(passed / total, 4) if total else 0.0,
        checks=checks,
        all_passed=passed == total and total > 0,
    )
