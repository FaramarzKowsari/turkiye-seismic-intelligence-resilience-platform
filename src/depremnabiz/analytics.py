from __future__ import annotations

import math

import numpy as np
import pandas as pd
from sklearn.cluster import DBSCAN

EARTH_RADIUS_KM = 6371.0088


def summary(frame: pd.DataFrame) -> dict[str, float | int | str | None]:
    if frame.empty:
        return {
            "events": 0,
            "max_magnitude": None,
            "median_depth_km": None,
            "shallow_share": None,
            "latest_event_utc": None,
        }
    magnitude = frame["magnitude"].dropna()
    depth = frame["depth_km"].dropna()
    return {
        "events": int(len(frame)),
        "max_magnitude": float(magnitude.max()) if not magnitude.empty else None,
        "median_depth_km": float(depth.median()) if not depth.empty else None,
        "shallow_share": float((depth <= 20).mean()) if not depth.empty else None,
        "latest_event_utc": frame["time_utc"].max().isoformat(),
    }


def daily_counts(frame: pd.DataFrame) -> pd.DataFrame:
    if frame.empty:
        return pd.DataFrame(columns=["date", "event_count", "max_magnitude"])
    indexed = frame.set_index("time_utc")
    counts = indexed.resample("1D").agg(
        event_count=("event_id", "count"),
        max_magnitude=("magnitude", "max"),
    )
    return counts.reset_index().rename(columns={"time_utc": "date"})


def rolling_rate_anomalies(
    frame: pd.DataFrame,
    baseline_days: int = 14,
    z_threshold: float = 2.5,
) -> pd.DataFrame:
    counts = daily_counts(frame)
    if counts.empty:
        counts["rolling_mean"] = []
        counts["rolling_std"] = []
        counts["z_score"] = []
        counts["anomaly"] = []
        return counts
    counts["rolling_mean"] = counts["event_count"].rolling(baseline_days, min_periods=3).mean()
    counts["rolling_std"] = counts["event_count"].rolling(baseline_days, min_periods=3).std(ddof=0)
    denominator = counts["rolling_std"].replace(0, np.nan)
    counts["z_score"] = (counts["event_count"] - counts["rolling_mean"]) / denominator
    counts["anomaly"] = counts["z_score"].abs() >= z_threshold
    return counts


def estimate_b_value(frame: pd.DataFrame, completeness_magnitude: float = 2.0) -> dict[str, float | int | None]:
    values = frame.loc[frame["magnitude"] >= completeness_magnitude, "magnitude"].dropna()
    if len(values) < 20:
        return {"b_value": None, "sample_size": int(len(values)), "mc": completeness_magnitude}
    mean_magnitude = float(values.mean())
    denominator = mean_magnitude - (completeness_magnitude - 0.05)
    if denominator <= 0:
        return {"b_value": None, "sample_size": int(len(values)), "mc": completeness_magnitude}
    b_value = math.log10(math.e) / denominator
    return {"b_value": float(b_value), "sample_size": int(len(values)), "mc": completeness_magnitude}


def spatial_clusters(
    frame: pd.DataFrame,
    eps_km: float = 35.0,
    min_samples: int = 4,
) -> pd.DataFrame:
    output = frame.copy()
    output["cluster"] = -1
    valid = output.dropna(subset=["latitude", "longitude"])
    if len(valid) < min_samples:
        return output
    coordinates = np.radians(valid[["latitude", "longitude"]].to_numpy())
    model = DBSCAN(
        eps=eps_km / EARTH_RADIUS_KM,
        min_samples=min_samples,
        metric="haversine",
    )
    labels = model.fit_predict(coordinates)
    output.loc[valid.index, "cluster"] = labels
    return output
