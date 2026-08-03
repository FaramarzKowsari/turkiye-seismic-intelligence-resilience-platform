from __future__ import annotations

from pathlib import Path

import pandas as pd
from fastapi import FastAPI, HTTPException, Query

from depremnabiz.analytics import estimate_b_value, summary
from depremnabiz.pipeline import clean_events, quality_report
from depremnabiz.providers.usgs import fetch_events

app = FastAPI(
    title="DepremNabız AI API",
    version="1.0.0",
    description="Read-only earthquake analytics API for research and demonstration.",
)

DEMO_PATH = Path(__file__).resolve().parents[2] / "data" / "demo" / "earthquakes.csv"


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "depremnabiz-ai"}


@app.get("/demo/summary")
def demo_summary() -> dict[str, object]:
    if not DEMO_PATH.exists():
        raise HTTPException(status_code=503, detail="Demo data has not been generated.")
    frame = clean_events(pd.read_csv(DEMO_PATH))
    return {
        "data_statement": "Synthetic demo data",
        "summary": summary(frame),
        "quality": quality_report(frame),
        "b_value": estimate_b_value(frame),
    }


@app.get("/live/usgs/summary")
def live_usgs_summary(
    days: int = Query(default=7, ge=1, le=90),
    min_magnitude: float = Query(default=2.0, ge=0, le=9),
) -> dict[str, object]:
    frame = clean_events(fetch_events(days=days, min_magnitude=min_magnitude))
    return {
        "source": "USGS Earthquake Catalog API",
        "summary": summary(frame),
        "quality": quality_report(frame),
        "b_value": estimate_b_value(frame, completeness_magnitude=min_magnitude),
    }
