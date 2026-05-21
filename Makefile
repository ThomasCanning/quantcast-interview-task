.PHONY: install global-install test run

VENV := .venv

install:
	python3 -m venv $(VENV)
	$(VENV)/bin/pip install -e ".[test]"

# pipx installs a Python CLI into its own venv but exposes it on PATH. Install with `brew install pipx`.
global-install:
	pipx install --force .

test:
	$(VENV)/bin/pytest

run:
	$(VENV)/bin/most-active-cookie -f example-cookies.csv -d 2026-05-15
