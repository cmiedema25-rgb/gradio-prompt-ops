# Proof of Skills

## Gradio

- `src/gradio_prompt_ops/ui.py` builds a Blocks app; `app.py` launches it.
- Tests smoke-import Gradio and call `build_app()` without opening a port in CI
  beyond the library import. Batch path never needs a browser.

## Prompt Engineering

- Authored A/B cases in `data/prompt_cases.jsonl` contrast creative vs grounded,
  free text vs JSON, and numbered checklists.
- Rubric enforces required terms, forbidden terms, JSON validity, numbered lists.

## Generative AI / Hugging Face-style local mock

- `mock_llm.py` is a deterministic local generator (no download, no API).
- Suitable stand-in for a local HF inference stub in demos.

## Python

- Core package has zero required deps; Gradio lives in `[ui]`.

## Reproduce

```bash
python -m pip install -e '.[dev,ui]'
make verify
```

Expected: 8/8 expected winners, B win rate 0.875, rubric pass B 0.875, Ruff clean.
