"""A/B prompt comparison against one user input and rubric."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from gradio_prompt_ops.mock_llm import generate
from gradio_prompt_ops.rubric import Rubric, ScoreCard, score_text


@dataclass
class PairResult:
    input: str
    prompt_a: str
    prompt_b: str
    output_a: str
    output_b: str
    score_a: ScoreCard
    score_b: ScoreCard
    winner: str
    delta: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "input": self.input,
            "prompt_a": self.prompt_a,
            "prompt_b": self.prompt_b,
            "output_a": self.output_a,
            "output_b": self.output_b,
            "score_a": asdict(self.score_a),
            "score_b": asdict(self.score_b),
            "winner": self.winner,
            "delta": self.delta,
        }


def compare_prompts(prompt_a: str, prompt_b: str, user: str, rubric: Rubric) -> PairResult:
    out_a = generate(prompt_a, user)
    out_b = generate(prompt_b, user)
    score_a = score_text(out_a, rubric)
    score_b = score_text(out_b, rubric)
    if score_b.score > score_a.score:
        winner = "B"
    elif score_a.score > score_b.score:
        winner = "A"
    else:
        winner = "tie"
    return PairResult(
        input=user,
        prompt_a=prompt_a,
        prompt_b=prompt_b,
        output_a=out_a,
        output_b=out_b,
        score_a=score_a,
        score_b=score_b,
        winner=winner,
        delta=round(score_b.score - score_a.score, 4),
    )
