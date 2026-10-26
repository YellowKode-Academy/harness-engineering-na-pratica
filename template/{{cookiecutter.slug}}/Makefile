.PHONY: test test-all lint smoke

test:
	pytest tests/unit -v

test-all:
	pytest -v

lint:
	ruff check .

smoke:
	python scripts/smoke_test.py
