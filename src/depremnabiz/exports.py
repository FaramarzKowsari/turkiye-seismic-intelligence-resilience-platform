from __future__ import annotations

import json
from pathlib import Path

import pandas as pd


def write_exports(frame: pd.DataFrame, output_dir: str | Path) -> dict[str, Path]:
    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)
    csv_path = output / "earthquakes.csv"
    xlsx_path = output / "earthquakes.xlsx"
    parquet_path = output / "earthquakes.parquet"
    geojson_path = output / "earthquakes.geojson"
    frame.to_csv(csv_path, index=False)
    frame.to_excel(xlsx_path, index=False)
    frame.to_parquet(parquet_path, index=False)
    features = []
    for _, row in frame.dropna(subset=["latitude", "longitude"]).iterrows():
        properties = row.drop(labels=["latitude", "longitude"]).to_dict()
        for key, value in list(properties.items()):
            if hasattr(value, "isoformat"):
                properties[key] = value.isoformat()
            elif pd.isna(value):
                properties[key] = None
        features.append(
            {
                "type": "Feature",
                "geometry": {"type": "Point", "coordinates": [row["longitude"], row["latitude"]]},
                "properties": properties,
            }
        )
    geojson_path.write_text(
        json.dumps({"type": "FeatureCollection", "features": features}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return {"csv": csv_path, "xlsx": xlsx_path, "parquet": parquet_path, "geojson": geojson_path}
