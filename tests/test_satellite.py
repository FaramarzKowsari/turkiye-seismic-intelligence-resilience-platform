import pandas as pd

from depremnabiz.satellite import build_pair_plan, summarise_displacement


def test_pair_plan_and_displacement_summary():
    catalogue = pd.DataFrame(
        {
            "item_id": ["a", "b", "c"],
            "datetime": pd.to_datetime(["2026-01-01", "2026-01-13", "2026-01-25"], utc=True),
            "relative_orbit": [87, 87, 87],
            "orbit_state": ["ascending"] * 3,
        }
    )
    pairs = build_pair_plan(catalogue, max_gap_days=15)
    assert len(pairs) == 2
    summary = summarise_displacement(pd.DataFrame({"displacement_mm": [-5, 0, 10]}))
    assert summary["points"] == 3
    assert summary["max_mm"] == 10
