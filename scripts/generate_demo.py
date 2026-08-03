from __future__ import annotations

from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "data" / "demo"
OUTPUT.mkdir(parents=True, exist_ok=True)

rng = np.random.default_rng(20260803)
start = datetime.now(timezone.utc) - timedelta(days=120)
centres = [
    (40.85, 29.25, "Marmara synthetic cluster"),
    (38.45, 27.25, "Aegean synthetic cluster"),
    (37.35, 37.05, "Southeast synthetic cluster"),
    (39.65, 39.50, "Eastern Anatolia synthetic cluster"),
]
rows = []
for index in range(620):
    centre_lat, centre_lon, place = centres[index % len(centres)]
    time = start + timedelta(hours=float(rng.uniform(0, 120 * 24)))
    magnitude = float(np.clip(rng.exponential(0.55) + 1.2, 1.0, 5.8))
    if index in {144, 145, 146, 310, 311}:
        magnitude += 1.4
    rows.append(
        {
            "event_id": f"demo-{index:04d}",
            "time_utc": time.isoformat(),
            "latitude": centre_lat + rng.normal(0, 0.42),
            "longitude": centre_lon + rng.normal(0, 0.55),
            "depth_km": float(np.clip(rng.gamma(2.1, 5.2), 1.0, 65.0)),
            "magnitude": round(magnitude, 2),
            "magnitude_type": "Mw-demo",
            "place": place,
            "source": "SYNTHETIC_DEMO",
            "url": "",
        }
    )
pd.DataFrame(rows).sort_values("time_utc").to_csv(OUTPUT / "earthquakes.csv", index=False)

exposure_centres = [
    (41.01, 28.97, "Synthetic metro population", "population", 1500),
    (40.77, 29.95, "Synthetic industrial area", "industry", 850),
    (38.42, 27.14, "Synthetic hospital group", "health", 500),
    (37.58, 36.93, "Synthetic shelter inventory", "shelter", 620),
    (39.75, 39.49, "Synthetic transport node", "transport", 430),
]
exposure_rows = []
for index in range(180):
    latitude, longitude, name, category, weight = exposure_centres[index % len(exposure_centres)]
    exposure_rows.append(
        {
            "name": f"{name} {index + 1}",
            "category": category,
            "latitude": latitude + rng.normal(0, 0.18),
            "longitude": longitude + rng.normal(0, 0.22),
            "weight": max(10, int(weight * rng.uniform(0.45, 1.35))),
            "source": "SYNTHETIC_DEMO",
        }
    )
pd.DataFrame(exposure_rows).to_csv(OUTPUT / "exposure_points.csv", index=False)

satellite_rows = []
base_time = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=120)
for index in range(30):
    satellite_rows.append(
        {
            "item_id": f"S1-DEMO-{index:03d}",
            "datetime": (base_time + pd.Timedelta(days=6 * index)).isoformat(),
            "platform": "sentinel-1-demo",
            "orbit_state": "ascending" if index % 2 == 0 else "descending",
            "relative_orbit": 87 if index % 2 == 0 else 167,
            "instrument_mode": "IW",
            "polarizations": "VV, VH",
            "stac_url": "",
            "source": "SYNTHETIC_DEMO",
        }
    )
pd.DataFrame(satellite_rows).to_csv(OUTPUT / "sentinel_catalog.csv", index=False)

print(f"Generated demo data in {OUTPUT}")
