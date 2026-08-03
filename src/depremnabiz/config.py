from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TurkeyBounds:
    min_latitude: float = 35.5
    max_latitude: float = 43.0
    min_longitude: float = 25.0
    max_longitude: float = 46.5


TURKEY_BOUNDS = TurkeyBounds()
DEFAULT_USER_AGENT = "DepremNabizAI/1.0 (research software; github.com/FaramarzKowsari)"
