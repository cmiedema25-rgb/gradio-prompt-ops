# Gradio Prompt Ops — Loom script (~2 minutes)

**Repo:** https://github.com/cmiedema25-rgb/gradio-prompt-ops  
**Suggested title:** Gradio Prompt Ops — A/B win rate 0.875 offline

---

## Hook (0:00–0:18)
Prompt changes ship without a repeatable A/B rubric. I built a Gradio lab that
compares two system prompts against a deterministic mock LLM — no API key.

## What you built (0:18–0:35)
Template mock LLM reacts to “concise / JSON / numbered / do not promise”.
Rubric scores required and forbidden terms. CLI batch mode keeps CI offline;
Gradio is for interactive demos.

## Live demo beats (0:35–1:40)

```bash
cd gradio-prompt-ops
python -m venv .venv && source .venv/bin/activate
python -m pip install -e ".[dev,ui]"
prompt-ops batch --report evidence/prompt-ops-report.json
```

**On-screen numbers (synthetic / authored — honest):**
- Cases: **8**
- Expected winners matched: **8/8**
- Prompt B wins: **7** (win rate **0.875**)
- Rubric pass B: **7/8** (rate **0.875**)
- Prompt A wins: **1** (grounded vs creative swap case)

Optional UI beat: `python app.py` → click Compare A/B on the default delay fixture.

**ROI framing:** On these eight fixtures, grounded prompts stop “guarantee”
hallucinations that creative prompts invent — fewer manual re-reads of the same
ops copy. Scenario savings on authored checks — not customer ROI.

```bash
make verify
```

## Close (1:40–2:05)
Reproduce with `make verify`.  
GitHub: https://github.com/cmiedema25-rgb/gradio-prompt-ops  
Results prove the A/B lab on a mock LLM — not production model quality.
