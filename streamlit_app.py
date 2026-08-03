from pathlib import Path

exec((Path(__file__).parent / "app" / "streamlit_app.py").read_text(encoding="utf-8"))
