"""Gradio Blocks UI for interactive prompt A/B comparison."""

from __future__ import annotations

from typing import Any

from gradio_prompt_ops.compare import compare_prompts
from gradio_prompt_ops.rubric import Rubric

DEFAULT_A = "Write a creative punchy customer update."
DEFAULT_B = (
    "Write a concise ops update. Must include the load id and delay hours. "
    "Do not promise ETAs. Do not invent facts."
)
DEFAULT_INPUT = (
    "Load LW-441 from Chicago to Dallas is 6 hours late. "
    "Driver cited traffic. Customer is Cascadia."
)


def compare_ui(
    prompt_a: str,
    prompt_b: str,
    user_input: str,
    required: str,
    forbidden: str,
    requires_json: bool,
    requires_numbered: bool,
) -> tuple[str, str, str, dict[str, Any]]:
    rubric = Rubric(
        required_terms=[t.strip() for t in required.split(",") if t.strip()],
        forbidden_terms=[t.strip() for t in forbidden.split(",") if t.strip()],
        requires_json=bool(requires_json),
        requires_numbered_list=bool(requires_numbered),
    )
    pair = compare_prompts(prompt_a, prompt_b, user_input, rubric)
    scores = {
        "winner": pair.winner,
        "score_a": pair.score_a.score,
        "score_b": pair.score_b.score,
        "pass_a": pair.score_a.all_passed,
        "pass_b": pair.score_b.all_passed,
        "delta": pair.delta,
        "checks_a": [c.__dict__ for c in pair.score_a.checks],
        "checks_b": [c.__dict__ for c in pair.score_b.checks],
    }
    return pair.output_a, pair.output_b, pair.winner, scores


def build_app():
    import gradio as gr

    with gr.Blocks(title="Prompt Ops Lab") as demo:
        gr.Markdown(
            "# Prompt Ops Lab\n"
            "A/B compare prompt instructions against a **deterministic mock LLM**. "
            "No API key. Batch/CI path: `prompt-ops batch` / `make verify`."
        )
        with gr.Row():
            prompt_a = gr.Textbox(label="Prompt A", value=DEFAULT_A, lines=5)
            prompt_b = gr.Textbox(label="Prompt B", value=DEFAULT_B, lines=5)
        user_input = gr.Textbox(label="User input / fixture", value=DEFAULT_INPUT, lines=3)
        with gr.Row():
            required = gr.Textbox(label="Required terms (comma-separated)", value="LW-441, 6")
            forbidden = gr.Textbox(label="Forbidden terms", value="guarantee")
        with gr.Row():
            requires_json = gr.Checkbox(label="Requires JSON")
            requires_numbered = gr.Checkbox(label="Requires numbered list")
        btn = gr.Button("Compare A/B", variant="primary")
        with gr.Row():
            out_a = gr.Textbox(label="Output A", lines=6)
            out_b = gr.Textbox(label="Output B", lines=6)
        winner = gr.Textbox(label="Winner")
        scores = gr.JSON(label="Scorecard")
        btn.click(
            compare_ui,
            inputs=[
                prompt_a,
                prompt_b,
                user_input,
                required,
                forbidden,
                requires_json,
                requires_numbered,
            ],
            outputs=[out_a, out_b, winner, scores],
        )
    return demo
