<p align="center">
  <img src="https://avatars.githubusercontent.com/u/105053743?v=4&s=256" width="128" height="128" alt="Faramarz Kowsari">
</p>

<h1 align="center">Türkiye Seismic Intelligence &amp; Resilience Platform</h1>
<p align="center"><strong>DepremNabız AI</strong> · Open-Source Earthquake Analytics, Satellite Deformation Monitoring and Urban Exposure Intelligence for Türkiye</p>

<p align="center">
  <a href="https://github.com/FaramarzKowsari/turkiye-seismic-intelligence-resilience-platform/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/FaramarzKowsari/turkiye-seismic-intelligence-resilience-platform/actions/workflows/ci.yml/badge.svg"></a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-168D73.svg"></a>
  <img alt="Python 3.11+" src="https://img.shields.io/badge/Python-3.11%2B-3670A0.svg">
  <img alt="Data modes" src="https://img.shields.io/badge/Data-Demo%20%2B%20Live-f3b43f.svg">
  <img alt="Safety" src="https://img.shields.io/badge/Safety-No%20prediction-critical.svg">
</p>

<p align="center">
  <a href="#english">English</a> ·
  <a href="#türkçe">Türkçe</a> ·
  <a href="https://depremnabiz-ai.streamlit.app">Interactive App</a> ·
  <a href="https://faramarzkowsari.github.io/turkiye-seismic-intelligence-resilience-platform/">Project Website</a> ·
  <a href="docs/RELEASE_AND_ZENODO.md">Release & DOI</a>
</p>

> **Safety boundary:** this platform performs research analytics and exposure screening. It does
> not predict earthquakes, issue early warnings, certify buildings, estimate official losses or
> replace AFAD and other competent authorities.

---

<a id="english"></a>

## English

### What this project is

DepremNabız AI is a provider-aware, reproducible research platform for transforming earthquake
catalogues and geospatial inputs into transparent analytical products. It combines a public live
USGS feed restricted to the Türkiye region, optional AFAD-compatible ingestion, deterministic demo
data, Sentinel-1 catalogue discovery, deformation-point exploration, exposure screening, data
quality reports, exports, an interactive Streamlit application and a read-only FastAPI service.

### What works without registration

- Reproducible synthetic demo mode
- Live USGS Earthquake Catalog queries for Türkiye
- CSV / Excel / Parquet / GeoJSON-compatible local inputs
- Copernicus Data Space STAC catalogue discovery
- Interactive maps, charts, anomaly screening and exports
- GitHub Pages, CI, API, tests and release validation

Copernicus protected asset download may require a free account. AFAD data use must follow AFAD
attribution and access rules.

### Analytical capabilities

- Event cleaning, schema normalisation and UTC handling
- Missing, duplicate and coordinate-range validation
- Magnitude, depth and temporal-distribution summaries
- Rolling event-rate anomaly screening
- Gutenberg–Richter b-value estimation with visible assumptions
- DBSCAN spatial-cluster exploration
- Magnitude–depth and time-of-day analysis
- Live-event maps with explicit source and freshness labels
- Radius-based population/facility exposure screening from user-supplied point data
- Sentinel-1 GRD acquisition search and pair-planning manifests
- Uploaded InSAR displacement-point visualisation and summary statistics
- CSV, Excel, Parquet and GeoJSON exports

### Architecture

```text
Official/public catalogues ─┐
Local files and demo data ──┼─> validation ─> analytical layer ─> Streamlit / FastAPI / exports
Satellite catalogue ────────┘
```

Core stack: **Python, Pandas, NumPy, scikit-learn, Plotly, Streamlit, FastAPI,
GitHub Actions, GitHub Pages and Zenodo**.

### Quick start

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate

pip install -e ".[dev,app]"
python scripts/generate_demo.py
streamlit run app/streamlit_app.py
```

API:

```bash
uvicorn depremnabiz.api:app --reload
```

### Data source references

- AFAD Earthquake Department: https://deprem.afad.gov.tr/
- USGS Earthquake Catalog API: https://earthquake.usgs.gov/fdsnws/event/1/
- Copernicus Data Space STAC: https://stac.dataspace.copernicus.eu/v1/

---

<a id="türkçe"></a>

## Türkçe

### Proje nedir?

DepremNabız AI; deprem kataloglarını ve mekânsal girdileri şeffaf, izlenebilir ve tekrar
üretilebilir analitik ürünlere dönüştüren açık kaynaklı bir araştırma platformudur. Türkiye için
filtrelenmiş canlı USGS verisi, isteğe bağlı AFAD uyumlu veri girişi, sentetik demo modu,
Sentinel-1 katalog keşfi, deformasyon noktası incelemesi, kentsel maruziyet taraması, veri kalite
raporları, dışa aktarma araçları, Streamlit dashboard ve salt okunur FastAPI hizmetini bir araya
getirir.

### Kayıt gerektirmeden çalışan bölümler

- Tekrar üretilebilir sentetik demo verisi
- Türkiye için canlı USGS deprem kataloğu sorguları
- Yerel CSV / Excel / Parquet dosyaları
- Copernicus STAC üzerinden uydu ürünü keşfi
- Haritalar, grafikler, anomali taraması ve dışa aktarma
- GitHub Pages, testler, CI ve sürüm doğrulaması

Copernicus dosya indirme işlemleri ücretsiz bir hesap gerektirebilir. AFAD verileri kullanılırken
AFAD kaynak gösterme ve erişim kurallarına uyulmalıdır.

### Temel yetenekler

- Şema normalizasyonu, UTC zaman standardı ve veri kalite kontrolü
- Büyüklük, derinlik, zaman ve mekân analizi
- Hareketli olay oranı üzerinden anomali taraması
- Gutenberg–Richter b-değeri hesaplaması
- DBSCAN ile mekânsal küme araştırması
- Kullanıcı verisiyle nüfus, tesis ve altyapı maruziyet taraması
- Sentinel-1 ürün keşfi ve eşleştirme planı
- InSAR deplasman noktalarının haritalanması
- CSV, Excel, Parquet ve GeoJSON çıktıları

### Bilimsel sorumluluk

Platform deprem tahmini veya erken uyarı sistemi değildir. Sonuçlar keşifsel araştırma ve karar
destek prototiplemesi içindir; resmî afet yönetimi açıklamalarının yerine geçmez.

---

## Repository structure

```text
app/                 Streamlit application
src/depremnabiz/     providers, pipeline, analytics, exposure, satellite and API
scripts/             reproducible demo, exports and release audit
data/demo/           clearly labelled synthetic examples
docs/                bilingual GitHub Pages website and technical documents
tests/               automated behavioural and metadata tests
.github/workflows/   CI, Pages and release validation
```

## Author

**Faramarz Kowsari** is an author, Software Engineer and AI researcher based in Istanbul. Focusing
on the intersection of technology, education, and personal growth, he has published over 80 digital
titles on international platforms. His areas of expertise span Artificial Intelligence, prompt
engineering, modern trading strategies (Smart Money Concepts & algorithmic trading), as well as
classical literature and mindfulness. In addition to writing, he develops web-based educational
tools and creates specialized instructional video content.

Official profiles: [ORCID](https://orcid.org/0000-0003-1692-0453) ·
[Google Scholar](https://scholar.google.com/citations?user=G7tP5WMAAAAJ&hl=en) ·
[GitHub](https://github.com/FaramarzKowsari) ·
[LinkedIn](https://www.linkedin.com/in/faramarzkowsari) ·
[Google Books](https://play.google.com/store/search?q=Faramarz_Kowsari&c=books) ·
[Official Website](https://faramarzkowsari.github.io) ·
[Zenodo Records](https://zenodo.org/search?q=creators.orcid%3A%220000-0003-1692-0453%22&l=list&p=1&s=10&sort=bestmatch)

## Citation

See [`CITATION.cff`](CITATION.cff). After the first Zenodo DOI is minted, run:

```bash
python scripts/apply_zenodo_doi.py 10.5281/zenodo.YOUR_ID
```

## License

MIT License for source code. External data remains subject to provider terms and attribution rules.
