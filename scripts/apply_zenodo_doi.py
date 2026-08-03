from __future__ import annotations

import re
import sys
from pathlib import Path

if len(sys.argv) != 2:
    raise SystemExit("Usage: python scripts/apply_zenodo_doi.py 10.5281/zenodo.YOUR_ID")

doi = sys.argv[1].removeprefix("https://doi.org/")
root = Path(__file__).resolve().parents[1]

citation_path = root / "CITATION.cff"
citation = citation_path.read_text(encoding="utf-8")
if re.search(r'^doi:', citation, flags=re.M):
    citation = re.sub(r'^doi:.*$', f'doi: "{doi}"', citation, flags=re.M)
else:
    citation += f'\ndoi: "{doi}"\n'
citation_path.write_text(citation, encoding="utf-8")

readme_path = root / "README.md"
readme = readme_path.read_text(encoding="utf-8")
placeholder = "python scripts/apply_zenodo_doi.py 10.5281/zenodo.YOUR_ID"
readme = readme.replace(placeholder, f"Version DOI: https://doi.org/{doi}")
readme_path.write_text(readme, encoding="utf-8")

index_path = root / "docs" / "index.html"
index = index_path.read_text(encoding="utf-8")
index = re.sub(
    r'<meta name="citation_doi" content="[^"]*">',
    f'<meta name="citation_doi" content="{doi}">',
    index,
)
index_path.write_text(index, encoding="utf-8")
print(f"Applied DOI {doi}")
