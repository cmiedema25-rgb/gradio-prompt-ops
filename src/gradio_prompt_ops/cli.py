"""CLI: prompt-ops batch | compare."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from gradio_prompt_ops.batch import run_batch, write_report
from gradio_prompt_ops.compare import compare_prompts
from gradio_prompt_ops.rubric import Rubric


def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="prompt-ops")
    sub = parser.add_subparsers(dest="command", required=True)

    batch = sub.add_parser("batch", help="Run authored A/B cases (no browser)")
    batch.add_argument("--cases", default=str(_repo_root() / "data" / "prompt_cases.jsonl"))
    batch.add_argument(
        "--report", default=str(_repo_root() / "evidence" / "prompt-ops-report.json")
    )

    cmp = sub.add_parser("compare", help="Compare two prompts on one input")
    cmp.add_argument("--prompt-a", required=True)
    cmp.add_argument("--prompt-b", required=True)
    cmp.add_argument("--input", required=True)
    cmp.add_argument("--required", default="")
    cmp.add_argument("--forbidden", default="")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "compare":
        rubric = Rubric(
            required_terms=[t.strip() for t in args.required.split(",") if t.strip()],
            forbidden_terms=[t.strip() for t in args.forbidden.split(",") if t.strip()],
        )
        pair = compare_prompts(args.prompt_a, args.prompt_b, args.input, rubric)
        print(json.dumps(pair.to_dict(), indent=2))
        return 0
    report = run_batch(args.cases)
    dest = write_report(report, args.report)
    print(
        json.dumps(
            {
                "cases": report["cases"],
                "b_wins": report["b_wins"],
                "b_win_rate": report["b_win_rate"],
                "rubric_pass_b": report["rubric_pass_b"],
                "rubric_pass_rate_b": report["rubric_pass_rate_b"],
                "passed": report["passed"],
                "report": str(dest),
            },
            indent=2,
        )
    )
    return 0 if report["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
