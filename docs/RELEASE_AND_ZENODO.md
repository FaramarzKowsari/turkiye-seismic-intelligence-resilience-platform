# Release and Zenodo guide

1. Confirm `pytest` and `ruff check .` pass.
2. Run `python scripts/release_audit.py`.
3. Create tag `v1.0.0` and publish a GitHub Release.
4. Enable the repository in Zenodo's GitHub settings.
5. Zenodo archives the release and mints a version DOI plus a Concept DOI.
6. Run `python scripts/apply_zenodo_doi.py <version-doi>`.
7. Commit the updated README, CITATION and website metadata.

Recommended release title:

`DepremNabız AI v1.0.0 — Public Research Software Release`
