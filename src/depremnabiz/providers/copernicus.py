from __future__ import annotations

from datetime import date

import pandas as pd
import requests

from depremnabiz.config import DEFAULT_USER_AGENT

STAC_SEARCH = "https://stac.dataspace.copernicus.eu/v1/search"


def search_sentinel1(
    bbox: tuple[float, float, float, float],
    start_date: date,
    end_date: date,
    limit: int = 100,
    timeout: int = 30,
) -> pd.DataFrame:
    """Discover Sentinel-1 GRD acquisitions through the public Copernicus STAC catalogue."""
    body = {
        "collections": ["sentinel-1-grd"],
        "bbox": list(bbox),
        "datetime": f"{start_date.isoformat()}T00:00:00Z/{end_date.isoformat()}T23:59:59Z",
        "limit": limit,
        "sortby": [{"field": "datetime", "direction": "asc"}],
    }
    response = requests.post(
        STAC_SEARCH,
        json=body,
        headers={"User-Agent": DEFAULT_USER_AGENT},
        timeout=timeout,
    )
    response.raise_for_status()
    rows: list[dict[str, object]] = []
    for item in response.json().get("features", []):
        props = item.get("properties", {})
        rows.append(
            {
                "item_id": item.get("id"),
                "datetime": props.get("datetime") or props.get("start_datetime"),
                "platform": props.get("platform"),
                "orbit_state": props.get("sat:orbit_state"),
                "relative_orbit": props.get("sat:relative_orbit"),
                "instrument_mode": props.get("sar:instrument_mode"),
                "polarizations": ", ".join(props.get("sar:polarizations", []) or []),
                "stac_url": next(
                    (link.get("href") for link in item.get("links", []) if link.get("rel") == "self"),
                    None,
                ),
            }
        )
    frame = pd.DataFrame(rows)
    if not frame.empty:
        frame["datetime"] = pd.to_datetime(frame["datetime"], utc=True)
    return frame
