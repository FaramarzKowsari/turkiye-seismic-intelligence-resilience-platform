# Model card

## Included analytical models

1. Rolling event-rate z-score: screens for unusual catalogue activity relative to a rolling
   historical window.
2. DBSCAN spatial clustering: explores dense groups of epicentres using a haversine-distance
   approximation.
3. Gutenberg–Richter b-value estimate: descriptive catalogue statistic above a chosen completeness
   threshold.

## Not included

- Deterministic earthquake prediction
- Official aftershock probability forecasts
- Structural fragility or loss models
- Early warning

## Limitations

Catalogue completeness, provider updates, magnitude revisions, network coverage and geographic
filtering materially affect outputs. Model outputs are exploratory and must be interpreted by
qualified domain experts.
