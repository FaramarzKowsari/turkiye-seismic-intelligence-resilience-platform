import pandas as pd

from depremnabiz.pipeline import clean_events, normalise_events, quality_report


def test_normalise_and_clean_events():
    raw = pd.DataFrame(
        {
            "EventID": ["a", "a", "b"],
            "Date(UTC)": ["2026-01-01", "2026-01-01", "bad"],
            "Latitude": [40.0, 40.0, 95.0],
            "Longitude": [29.0, 29.0, 30.0],
            "Depth": [10, 10, 20],
            "Magnitude": [3.2, 3.2, 4.0],
        }
    )
    normalised = normalise_events(raw, source="TEST")
    cleaned = clean_events(normalised)
    assert list(cleaned["event_id"]) == ["a"]
    report = quality_report(normalised)
    assert report["duplicate_event_ids"] == 1
    assert report["invalid_coordinates"] == 1
