from __future__ import annotations

import re

import numpy as np
import pandas as pd

CANONICAL_COLUMNS = [
    "event_id",
    "time_utc",
    "latitude",
    "longitude",
    "depth_km",
    "magnitude",
    "magnitude_type",
    "place",
    "source",
    "url",
]

ALIASES = {
    "event_id": ["event_id", "eventid", "id", "event id"],
    "time_utc": ["time_utc", "time", "date", "datetime", "date(utc)", "origin time"],
    "latitude": ["latitude", "lat", "enlem"],
    "longitude": ["longitude", "lon", "lng", "boylam"],
    "depth_km": ["depth_km", "depth", "derinlik"],
    "magnitude": ["magnitude", "mag", "büyüklük", "buyukluk"],
    "magnitude_type": ["magnitude_type", "magtype", "type", "tip"],
    "place": ["place", "location", "yer"],
    "url": ["url", "link"],
}


def _key(name: object) -> str:
    text = str(name).strip().lower()
    return re.sub(r"[^a-z0-9çğıöşü]+", " ", text).strip()


def normalise_events(raw: pd.DataFrame, source: str = "LOCAL") -> pd.DataFrame:
    mapping: dict[str, str] = {}
    keyed = {_key(column): column for column in raw.columns}
    for canonical, aliases in ALIASES.items():
        for alias in aliases:
            if _key(alias) in keyed:
                mapping[keyed[_key(alias)]] = canonical
                break
    frame = raw.rename(columns=mapping).copy()
    if "event_id" not in frame:
        frame["event_id"] = [f"{source.lower()}-{index}" for index in range(len(frame))]
    if "source" not in frame:
        frame["source"] = source
    for column in CANONICAL_COLUMNS:
        if column not in frame:
            frame[column] = np.nan
    frame["time_utc"] = pd.to_datetime(frame["time_utc"], utc=True, errors="coerce")
    for column in ["latitude", "longitude", "depth_km", "magnitude"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame["source"] = frame["source"].fillna(source).astype(str)
    frame = frame[CANONICAL_COLUMNS + [c for c in frame.columns if c not in CANONICAL_COLUMNS]]
    return frame.sort_values("time_utc").reset_index(drop=True)


def quality_report(frame: pd.DataFrame) -> dict[str, float | int]:
    if frame.empty:
        return {
            "rows": 0,
            "valid_time_share": 0.0,
            "valid_coordinate_share": 0.0,
            "magnitude_completeness": 0.0,
            "duplicate_event_ids": 0,
            "invalid_coordinates": 0,
        }
    valid_coordinates = frame["latitude"].between(-90, 90) & frame["longitude"].between(-180, 180)
    return {
        "rows": int(len(frame)),
        "valid_time_share": float(frame["time_utc"].notna().mean()),
        "valid_coordinate_share": float(valid_coordinates.mean()),
        "magnitude_completeness": float(frame["magnitude"].notna().mean()),
        "duplicate_event_ids": int(frame["event_id"].duplicated().sum()),
        "invalid_coordinates": int((~valid_coordinates).sum()),
    }


def clean_events(frame: pd.DataFrame) -> pd.DataFrame:
    clean = normalise_events(frame, source=str(frame.get("source", pd.Series(["LOCAL"])).iloc[0]))
    clean = clean.dropna(subset=["time_utc", "latitude", "longitude"])
    clean = clean[clean["latitude"].between(-90, 90) & clean["longitude"].between(-180, 180)]
    clean = clean.drop_duplicates(subset=["event_id"], keep="last")
    return clean.sort_values("time_utc").reset_index(drop=True)
