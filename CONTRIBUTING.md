# Contributing

1. Create a focused branch.
2. Add or update tests for behavioural changes.
3. Run `pytest` and `ruff check .`.
4. Keep provider adapters isolated from analytical logic.
5. Label demo, derived and official data clearly.
6. Never claim deterministic earthquake prediction.
7. Document units, coordinate reference systems, time zones and provenance.

Useful commands:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e ".[dev,app]"
pytest
ruff check .
streamlit run app/streamlit_app.py
```
