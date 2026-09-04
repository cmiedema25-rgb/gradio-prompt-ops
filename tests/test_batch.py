import json
from pathlib import Path

from gradio_prompt_ops.batch import run_batch
from gradio_prompt_ops.cli import main

ROOT = Path(__file__).resolve().parents[1]


def test_batch_matches_expected_winners() -> None:
    report = run_batch(ROOT / "data/prompt_cases.jsonl")
    misses = [r["id"] for r in report["results"] if not r["match_expected"]]
    assert misses == []
    assert report["cases"] == 8
    assert report["b_wins"] == 7
    assert report["a_wins"] == 1
    assert report["rubric_pass_b"] == 7
    assert report["passed"]


def test_cli_batch(tmp_path: Path) -> None:
    dest = tmp_path / "prompt-ops-report.json"
    assert (
        main(["batch", "--cases", str(ROOT / "data/prompt_cases.jsonl"), "--report", str(dest)])
        == 0
    )
    payload = json.loads(dest.read_text(encoding="utf-8"))
    assert payload["b_win_rate"] == 0.875
