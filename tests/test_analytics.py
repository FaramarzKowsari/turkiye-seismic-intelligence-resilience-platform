import pandas as pd

from depremnabiz.analytics import estimate_b_value, rolling_rate_anomalies, spatial_clusters


def sample_events() -> pd.DataFrame:
    times = pd.date_range("2026-01-01", periods=60, freq="12h", tz="UTC")
    return pd.DataFrame(
        {
            "event_id": [f"e{i}" for i in range(len(times))],
            "time_utc": times,
            "latitude": [40.0 + (i % 3) * 0.01 for i in range(len(times))],
            "longitude": [29.0 + (i % 3) * 0.01 for i in range(len(times))],
            "depth_km": [10.0] * len(times),
            "magnitude": [2.1 + (i % 10) * 0.1 for i in range(len(times))],
        }
    )


def test_b_value_and_anomaly_frame():
    frame = sample_events()
    result = estimate_b_value(frame, completeness_magnitude=2.0)
    assert result["b_value"] is not None
    anomaly = rolling_rate_anomalies(frame)
    assert "z_score" in anomaly


def test_spatial_clusters_assigns_labels():
    clustered = spatial_clusters(sample_events(), eps_km=10, min_samples=3)
    assert (clustered["cluster"] >= 0).any()
