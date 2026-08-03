from __future__ import annotations

from pathlib import Path

import pandas as pd

from depremnabiz.exports import write_exports
from depremnabiz.pipeline import clean_events

ROOT = Path(__file__).resolve().parents[1]
frame = clean_events(pd.read_csv(ROOT / "data" / "demo" / "earthquakes.csv"))
paths = write_exports(frame, ROOT / "outputs" / "demo")
for name, path in paths.items():
    print(f"{name}: {path}")
