PYTHON ?= python

.PHONY: install lint test batch verify ui

install:
	$(PYTHON) -m pip install -e '.[dev,ui]'

lint:
	ruff check .
	ruff format --check .

test:
	pytest --cov=gradio_prompt_ops --cov-report=term-missing --cov-fail-under=85 -q

batch:
	prompt-ops batch --report evidence/prompt-ops-report.json

ui:
	$(PYTHON) app.py

verify: lint test batch
