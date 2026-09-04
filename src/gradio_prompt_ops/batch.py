"""CLI/CI batch evaluation that does not need a browser."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from gradio_prompt_ops.compare import compare_prompts
from gradio_prompt_ops.rubric import Rubric


def load_cases(path: str | Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in Path(path).read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def run_batch(cases_path: str | Path) -> dict[str, Any]:
    rows = []
    for case in load_cases(cases_path):
        rubric = Rubric.from_dict(case["rubric"])
        pair = compare_prompts(case["prompt_a"], case["prompt_b"], case["input"], rubric)
        rows.append(
            {
                "id": case["id"],
                "winner": pair.winner,
                "score_a": pair.score_a.score,
                "score_b": pair.score_b.score,
                "pass_a": pair.score_a.all_passed,
                "pass_b": pair.score_b.all_passed,
                "expected_winner": case.get("expected_winner"),
                "match_expected": case.get("expected_winner") in {None, pair.winner},
                "output_a": pair.output_a,
                "output_b": pair.output_b,
            }
        )
    n = len(rows)
    b_wins = sum(1 for r in rows if r["winner"] == "B")
    a_wins = sum(1 for r in rows if r["winner"] == "A")
    ties = sum(1 for r in rows if r["winner"] == "tie")
    rubric_b = sum(1 for r in rows if r["pass_b"])
    expected_ok = sum(1 for r in rows if r["match_expected"])
    return {
        "cases": n,
        "b_wins": b_wins,
        "a_wins": a_wins,
        "ties": ties,
        "b_win_rate": round(b_wins / n, 4) if n else 0.0,
        "rubric_pass_b": rubric_b,
        "rubric_pass_rate_b": round(rubric_b / n, 4) if n else 0.0,
        "rubric_pass_a": sum(1 for r in rows if r["pass_a"]),
        "expected_winner_matches": expected_ok,
        "passed": expected_ok == n and n > 0,
        "results": rows,
    }


def write_report(report: dict[str, Any], dest: str | Path) -> Path:
    path = Path(dest)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    return path
