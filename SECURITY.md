# Security policy

## Supported version

The latest release on the `main` branch is supported.

## Credential handling

- The demo and USGS live modes require no credentials.
- Never commit Copernicus, AFAD, cloud or database credentials.
- Store local secrets in `.env` or `.streamlit/secrets.toml`; both are ignored by Git.
- Hosted secrets belong only in the deployment provider's encrypted secret manager.

## Reporting a vulnerability

Open a private GitHub security advisory when available, or contact the maintainer through the
public profile links in the README. Do not publish exploitable details in a public issue.

## Safety boundary

This application is not an earthquake prediction, early-warning, emergency response, building
safety certification or loss-estimation system. It must not be used as the sole basis for
life-safety decisions.
