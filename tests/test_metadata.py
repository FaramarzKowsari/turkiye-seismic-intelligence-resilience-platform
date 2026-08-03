import json
import tomllib
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def test_citation_and_zenodo_metadata():
    citation = yaml.safe_load((ROOT / "CITATION.cff").read_text(encoding="utf-8"))
    zenodo = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    pyproject = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert citation["authors"][0]["orcid"].endswith("0000-0003-1692-0453")
    assert zenodo["creators"][0]["orcid"] == "0000-0003-1692-0453"
    assert citation["version"] == pyproject["project"]["version"]


def test_bilingual_site_files_exist():
    index = (ROOT / "docs" / "index.html").read_text(encoding="utf-8")
    assert 'data-lang="en"' in index
    assert 'data-lang="tr"' in index
    assert "Faramarz Kowsari" in index
    assert (ROOT / "docs" / "robots.txt").exists()
    assert (ROOT / "docs" / "sitemap.xml").exists()
