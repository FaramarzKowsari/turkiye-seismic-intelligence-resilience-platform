from __future__ import annotations

import numpy as np
import pandas as pd

EARTH_RADIUS_KM = 6371.0088


def haversine_km(lat1: float, lon1: float, lat2: np.ndarray, lon2: np.ndarray) -> np.ndarray:
    phi1 = np.radians(lat1)
    phi2 = np.radians(lat2)
    delta_phi = np.radians(lat2 - lat1)
    delta_lambda = np.radians(lon2 - lon1)
    a = np.sin(delta_phi / 2) ** 2 + np.cos(phi1) * np.cos(phi2) * np.sin(delta_lambda / 2) ** 2
    return 2 * EARTH_RADIUS_KM * np.arctan2(np.sqrt(a), np.sqrt(1 - a))


def screen_exposure(
    events: pd.DataFrame,
    exposure_points: pd.DataFrame,
    radius_km: float = 50.0,
) -> pd.DataFrame:
    required = {"latitude", "longitude"}
    if not required.issubset(exposure_points.columns):
        raise ValueError("Exposure data must include latitude and longitude columns.")
    points = exposure_points.copy()
    points["weight"] = pd.to_numeric(points.get("weight", 1.0), errors="coerce").fillna(1.0)
    rows: list[dict[str, object]] = []
    for _, event in events.iterrows():
        distances = haversine_km(
            float(event["latitude"]),
            float(event["longitude"]),
            points["latitude"].to_numpy(dtype=float),
            points["longitude"].to_numpy(dtype=float),
        )
        mask = distances <= radius_km
        rows.append(
            {
                "event_id": event["event_id"],
                "magnitude": event.get("magnitude"),
                "nearby_points": int(mask.sum()),
                "exposure_weight": float(points.loc[mask, "weight"].sum()),
                "radius_km": radius_km,
            }
        )
    return pd.DataFrame(rows)
