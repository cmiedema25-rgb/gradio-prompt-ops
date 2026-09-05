# Gradio Prompt Ops

[![CI](https://github.com/cmiedema25-rgb/gradio-prompt-ops/actions/workflows/ci.yml/badge.svg)](https://github.com/cmiedema25-rgb/gradio-prompt-ops/actions/workflows/ci.yml)

Compare two system prompts on the same fixtures, score them with a rubric, and keep a batch report for CI. Includes a Gradio UI plus a headless CLI so Actions never needs a browser.

Uses a deterministic mock LLM (template-based) — no API key.

## Install

```bash
python -m venv .venv && source .venv/bin/activate
python -m pip install -e '.[dev,ui]'
make verify
```

## Usage

```bash
prompt-ops batch --report evidence/prompt-ops-report.json
prompt-ops compare --prompt-a "..." --prompt-b "..." --input "..." \
  --required "LW-441,6" --forbidden "guarantee"
python app.py   # Gradio UI
```

## Notes

Mock model is for repeatable prompt experiments, not production generation quality. Fixture set is small and authored on purpose.

## License

MIT
