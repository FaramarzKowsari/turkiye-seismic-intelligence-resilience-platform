from __future__ import annotations

import pandas as pd


def build_pair_plan(catalogue: pd.DataFrame, max_gap_days: int = 24) -> pd.DataFrame:
    """Create same-orbit chronological acquisition pairs for downstream InSAR workflows."""
    if catalogue.empty:
        return pd.DataFrame(
            columns=["reference_id", "secondary_id", "reference_time", "secondary_time", "gap_days"]
        )
    frame = catalogue.copy().sort_values("datetime")
    pairs: list[dict[str, object]] = []
    group_columns = [column for column in ["relative_orbit", "orbit_state"] if column in frame]
    grouped = frame.groupby(group_columns, dropna=False) if group_columns else [(None, frame)]
    for _, group in grouped:
        group = group.sort_values("datetime")
        for index in range(len(group) - 1):
            reference = group.iloc[index]
            secondary = group.iloc[index + 1]
            gap_days = (secondary["datetime"] - reference["datetime"]).total_seconds() / 86400
            if gap_days <= max_gap_days:
                pairs.append(
                    {
                        "reference_id": reference["item_id"],
                        "secondary_id": secondary["item_id"],
                        "reference_time": reference["datetime"],
                        "secondary_time": secondary["datetime"],
                        "gap_days": gap_days,
                        "relative_orbit": reference.get("relative_orbit"),
                        "orbit_state": reference.get("orbit_state"),
                    }
                )
    return pd.DataFrame(pairs)


def summarise_displacement(points: pd.DataFrame) -> dict[str, float | int | None]:
    if "displacement_mm" not in points:
        raise ValueError("Displacement input must include displacement_mm.")
    values = pd.to_numeric(points["displacement_mm"], errors="coerce").dropna()
    if values.empty:
        return {"points": 0, "median_mm": None, "min_mm": None, "max_mm": None, "p95_abs_mm": None}
    return {
        "points": int(len(values)),
        "median_mm": float(values.median()),
        "min_mm": float(values.min()),
        "max_mm": float(values.max()),
        "p95_abs_mm": float(values.abs().quantile(0.95)),
    }
