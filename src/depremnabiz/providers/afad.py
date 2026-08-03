from __future__ import annotations

from pathlib import Path

import pandas as pd

from depremnabiz.pipeline import normalise_events


def load_afad_export(path: str | Path) -> pd.DataFrame:
    """Load a user-downloaded AFAD catalogue export without relying on an undocumented endpoint."""
    path = Path(path)
    if path.suffix.lower() in {".xlsx", ".xls"}:
        raw = pd.read_excel(path)
    else:
        raw = pd.read_csv(path)
    return normalise_events(raw, source="AFAD")
