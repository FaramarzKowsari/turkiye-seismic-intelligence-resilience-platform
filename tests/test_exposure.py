import pandas as pd

from depremnabiz.exposure import screen_exposure


def test_exposure_screening():
    events = pd.DataFrame(
        {"event_id": ["e1"], "latitude": [40.0], "longitude": [29.0], "magnitude": [4.0]}
    )
    points = pd.DataFrame(
        {
            "latitude": [40.01, 42.0],
            "longitude": [29.01, 35.0],
            "weight": [100, 500],
        }
    )
    result = screen_exposure(events, points, radius_km=10)
    assert result.loc[0, "nearby_points"] == 1
    assert result.loc[0, "exposure_weight"] == 100
