# Gradio Prompt Ops

[![CI](https://github.com/cmiedema25-rgb/gradio-prompt-ops/actions/workflows/ci.yml/badge.svg)](https://github.com/cmiedema25-rgb/gradio-prompt-ops/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-3776AB.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

Gradio app for **prompt A/B comparison** and rubric scoring against a
deterministic mock LLM (template-based, Hugging Face-style local mock). Also
ships a CLI batch mode so CI never needs a browser.

## Reviewer proof in 60 seconds

| Verifiable outcome | Retained evidence | Reproduce |
| --- | --- | --- |
| 8/8 expected A/B winners matched | [`evidence/prompt-ops-report.json`](evidence/prompt-ops-report.json) | `make batch` |
| Prompt B win rate 0.875 (7/8) | same report | `make batch` |
| Rubric pass rate B 0.875 (7/8) | same report | `make batch` |
| Tests + Ruff green (Gradio import smoke) | [`evidence/VERIFICATION.md`](evidence/VERIFICATION.md) | `make verify` |

```bash
python -m venv .venv && source .venv/bin/activate
python -m pip install -e '.[dev,ui]'
make verify
```

## Problem → measurable demo

Prompt changes are hard to compare without a repeatable rubric. This lab scores
two system prompts on the same fixture and records win rates. Creative prompts
that invent “we guarantee…” fail the forbidden-term check; grounded prompts win.

## Skills demonstrated

- **Gradio:** `app.py` + `ui.py` Blocks UI for interactive A/B.
- **Prompt Engineering:** instruction styles (concise, JSON, numbered, no-promise).
- **Generative AI:** deterministic mock LLM reacting to prompt instructions.
- **Python:** CLI batch path; optional `[ui]` extra; pytest; Ruff; Actions.

## Architecture

```text
Prompt A / Prompt B + user fixture
        │
   mock LLM (template)
        │
   rubric scorecards ──► winner A|B|tie
        │
   Gradio UI  -or-  prompt-ops batch (CI)
```

## CLI / UI

```bash
prompt-ops batch --report evidence/prompt-ops-report.json
prompt-ops compare --prompt-a "..." --prompt-b "..." --input "..." \
  --required "LW-441,6" --forbidden "guarantee"
python app.py   # Gradio UI
```

## Limitations (honest)

- Mock LLM is template-based — not a hosted model or fine-tune.
- Gradio is optional (`[ui]` extra); CI uses batch mode.
- Eight authored pairs prove mechanics — not production prompt quality or ROI.
- See [`docs/PROOF_OF_SKILLS.md`](docs/PROOF_OF_SKILLS.md) and [`VIDEO_SCRIPT.md`](VIDEO_SCRIPT.md).
