from __future__ import annotations

from pydantic import BaseModel, Field


class EventRecord(BaseModel):
    event_id: str
    time_utc: str
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    depth_km: float | None = None
    magnitude: float | None = None
    magnitude_type: str | None = None
    place: str | None = None
    source: str
    url: str | None = None
