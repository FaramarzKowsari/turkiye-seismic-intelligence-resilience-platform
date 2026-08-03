from __future__ import annotations

import json
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

required = [
    "README.md",
    "LICENSE",
    "SECURITY.md",
    "DATA_LICENSE.md",
    "CITATION.cff",
    ".zenodo.json",
    "pyproject.toml",
    "docs/index.html",
    "data/demo/earthquakes.csv",
]
missing = [path for path in required if not (ROOT / path).exists()]
if missing:
    raise SystemExit(f"Missing required files: {missing}")

pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
citation = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
zenodo = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
assert citation["version"] == pyproject["project"]["version"]
assert citation["authors"][0]["orcid"].endswith("0000-0003-1692-0453")
assert zenodo["creators"][0]["orcid"] == "0000-0003-1692-0453"
print("Release audit passed.")
