from gradio_prompt_ops.mock_llm import generate
from gradio_prompt_ops.rubric import Rubric, score_text

LOAD = (
    "Load LW-441 from Chicago to Dallas is 6 hours late. "
    "Driver cited traffic. Customer is Cascadia."
)


def test_creative_prompt_adds_guarantee() -> None:
    text = generate(
        "Write a creative punchy customer update.",
        LOAD,
    )
    assert "LW-441" in text
    assert "guarantee" in text.lower()


def test_grounded_prompt_omits_guarantee() -> None:
    text = generate(
        "Write a concise ops update. Do not promise ETAs. Do not invent facts.",
        LOAD,
    )
    assert "LW-441" in text
    assert "guarantee" not in text.lower()


def test_json_mode() -> None:
    text = generate(
        "Respond with JSON only.", "Invoice INV-2207 vendor: Harbor Hardware total: 174.36"
    )
    assert text.startswith("{")
    assert "INV-2207" in text


def test_rubric_forbidden() -> None:
    rubric = Rubric(required_terms=["LW-441"], forbidden_terms=["guarantee"])
    bad = score_text("LW-441 We guarantee arrival tonight.", rubric)
    good = score_text("LW-441 is 6 hours delayed.", rubric)
    assert not bad.all_passed
    assert good.all_passed
