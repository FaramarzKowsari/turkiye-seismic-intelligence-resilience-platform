from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pandas as pd
import requests

from depremnabiz.config import DEFAULT_USER_AGENT, TURKEY_BOUNDS

USGS_ENDPOINT = "https://earthquake.usgs.gov/fdsnws/event/1/query"


def fetch_events(
    days: int = 30,
    min_magnitude: float = 1.5,
    timeout: int = 30,
) -> pd.DataFrame:
    """Fetch GeoJSON events from the official USGS FDSN service for Türkiye's bounding box."""
    end = datetime.now(UTC)
    start = end - timedelta(days=days)
    params = {
        "format": "geojson",
        "starttime": start.isoformat(),
        "endtime": end.isoformat(),
        "minmagnitude": min_magnitude,
        "minlatitude": TURKEY_BOUNDS.min_latitude,
        "maxlatitude": TURKEY_BOUNDS.max_latitude,
        "minlongitude": TURKEY_BOUNDS.min_longitude,
        "maxlongitude": TURKEY_BOUNDS.max_longitude,
        "orderby": "time-asc",
        "limit": 20000,
    }
    response = requests.get(
        USGS_ENDPOINT,
        params=params,
        headers={"User-Agent": DEFAULT_USER_AGENT},
        timeout=timeout,
    )
    response.raise_for_status()
    payload = response.json()
    rows: list[dict[str, object]] = []
    for feature in payload.get("features", []):
        props = feature.get("properties", {})
        coords = feature.get("geometry", {}).get("coordinates", [None, None, None])
        rows.append(
            {
                "event_id": feature.get("id"),
                "time_utc": pd.to_datetime(props.get("time"), unit="ms", utc=True),
                "latitude": coords[1],
                "longitude": coords[0],
                "depth_km": coords[2],
                "magnitude": props.get("mag"),
                "magnitude_type": props.get("magType"),
                "place": props.get("place"),
                "source": "USGS",
                "url": props.get("url"),
                "status": props.get("status"),
                "updated_utc": pd.to_datetime(props.get("updated"), unit="ms", utc=True),
            }
        )
    return pd.DataFrame(rows)
