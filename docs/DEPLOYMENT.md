# Deployment

## Streamlit Community Cloud

- Repository: `FaramarzKowsari/turkiye-seismic-intelligence-resilience-platform`
- Branch: `main`
- Main file: `app/streamlit_app.py`
- Suggested URL: `depremnabiz-ai.streamlit.app`

No secrets are needed for demo or USGS mode.

## GitHub Pages

Use GitHub Actions as the Pages source. The workflow publishes the `docs/` directory.

## Local Docker

```bash
docker compose up --build
```
