.PHONY: install test lint demo app api exports audit

install:
	python -m pip install -e ".[dev,app]"

test:
	pytest

lint:
	ruff check .

demo:
	python scripts/generate_demo.py

app:
	streamlit run app/streamlit_app.py

api:
	uvicorn depremnabiz.api:app --reload

exports:
	python scripts/build_exports.py

audit:
	python scripts/release_audit.py
