import pytest

from gradio_prompt_ops.ui import compare_ui

LOAD = (
    "Load LW-441 from Chicago to Dallas is 6 hours late. "
    "Driver cited traffic. Customer is Cascadia."
)


pytest.importorskip("gradio")


def test_compare_ui_helper() -> None:
    out_a, out_b, winner, scores = compare_ui(
        "Write a creative punchy customer update.",
        "Write a concise ops update. Do not promise ETAs.",
        LOAD,
        "LW-441, 6",
        "guarantee",
        False,
        False,
    )
    assert winner == "B"
    assert "LW-441" in out_a
    assert scores["score_b"] > scores["score_a"]


def test_build_app_without_launch() -> None:
    from gradio_prompt_ops.ui import build_app

    demo = build_app()
    assert demo is not None
    assert getattr(demo, "blocks", None) is not None or demo.__class__.__name__ == "Blocks"
