<p align="center">
  <img
    src="https://avatars.githubusercontent.com/u/105053743?v=4&s=256"
    width="128"
    height="128"
    alt="Faramarz Kowsari"
  >
</p>

<h1 align="center">Türkiye Seismic Intelligence &amp; Resilience Platform</h1>

<p align="center">
<<<<<<< HEAD
  <a href="https://github.com/FaramarzKowsari/turkiye-seismic-intelligence-resilience-platform/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/FaramarzKowsari/turkiye-seismic-intelligence-resilience-platform/actions/workflows/ci.yml/badge.svg"></a>
  <a href="https://doi.org/10.5281/zenodo.21797833">
    <img
      alt="Zenodo DOI"
      src="https://zenodo.org/badge/DOI/10.5281/zenodo.21797833.svg"
    >
  </a>
  <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-168D73.svg"></a>
  <img alt="Python 3.11+" src="https://img.shields.io/badge/Python-3.11%2B-3670A0.svg">
  <img alt="Data modes" src="https://img.shields.io/badge/Data-Demo%20%2B%20Live-f3b43f.svg">
  <img alt="Safety" src="https://img.shields.io/badge/Safety-No%20prediction-critical.svg">
=======
  <strong>DepremNabız AI</strong><br>
  Open-Source Earthquake Analytics, Satellite Deformation Monitoring and
  Urban Exposure Intelligence for Türkiye
</p>

<p align="center">
  <a href="https://github.com/FaramarzKowsari/turkiye-seismic-intelligence-resilience-platform/actions/workflows/ci.yml">
    <img
      alt="CI"
      src="https://github.com/FaramarzKowsari/turkiye-seismic-intelligence-resilience-platform/actions/workflows/ci.yml/badge.svg"
    >
  </a>
  <a href="https://depremnabiz-turkiye.streamlit.app">
    <img
      alt="Launch Live App"
      src="https://img.shields.io/badge/Launch-Live%20App-FF4B4B?logo=streamlit&logoColor=white"
    >
  </a>
  <a href="LICENSE">
    <img
      alt="License: MIT"
      src="https://img.shields.io/badge/License-MIT-168D73.svg"
    >
  </a>
  <img
    alt="Python 3.11+"
    src="https://img.shields.io/badge/Python-3.11%2B-3670A0.svg"
  >
  <img
    alt="Live USGS"
    src="https://img.shields.io/badge/Data-Live%20USGS-0866C6.svg"
  >
  <img
    alt="Demo ready"
    src="https://img.shields.io/badge/Demo-Reproducible-F3B43F.svg"
  >
  <img
    alt="Responsible analytics"
    src="https://img.shields.io/badge/Safety-No%20Earthquake%20Prediction-critical.svg"
  >
>>>>>>> 476e000d9227549fc3dcd20b064e4a5556ddb826
</p>

<p align="center">
  <a href="#english">English</a> ·
  <a href="#türkçe">Türkçe</a> ·
  <a href="https://depremnabiz-turkiye.streamlit.app">Interactive App</a> ·
  <a href="https://faramarzkowsari.github.io/turkiye-seismic-intelligence-resilience-platform/">Project Website</a> ·
  <a href="https://github.com/FaramarzKowsari/turkiye-seismic-intelligence-resilience-platform">Source Repository</a> ·
  <a href="docs/RELEASE_AND_ZENODO.md">Release &amp; DOI</a>
</p>

> **Safety boundary:** This platform performs research analytics, catalogue exploration,
> satellite-acquisition discovery and exposure screening. It does not predict earthquakes,
> issue early warnings, certify buildings, estimate official losses or replace AFAD, USGS,
> local authorities, engineering inspections or emergency-management institutions.

---

<a id="english"></a>

## English

### Project overview

**DepremNabız AI** is an open-source research software platform for transforming earthquake
catalogues, satellite-acquisition metadata and user-supplied geospatial inputs into transparent,
auditable and reproducible analytical products.

The platform combines:

- Near-real-time earthquake catalogue analytics for Türkiye
- Reproducible synthetic demonstration data
- Local CSV and Excel catalogue ingestion
- Data cleaning, schema normalisation and quality reporting
- Temporal, magnitude, depth and spatial analysis
- Rolling event-rate anomaly screening
- Gutenberg–Richter b-value estimation
- DBSCAN-based spatial-cluster exploration
- Radius-based urban exposure screening
- Sentinel-1 acquisition discovery through Copernicus STAC
- Same-orbit satellite pair planning
- Processed InSAR displacement-point exploration
- Interactive Streamlit reporting
- Read-only FastAPI access
- CSV, Excel, Parquet and GeoJSON-compatible outputs
- Automated tests, CI, release validation and DOI-ready metadata

The software is designed for research, education, reproducible experimentation, public-sector
prototyping and technical portfolio development.

## Live online reporting

The public Streamlit application is available at:

### [Launch DepremNabız AI](https://depremnabiz-turkiye.streamlit.app)

The **Live USGS** mode retrieves recent earthquake records from the official USGS Earthquake
Catalog API and restricts the query to the geographical region of Türkiye.

Users can control:

- Live lookback period from 1 to 90 days
- Minimum earthquake magnitude
- Data mode: Demo, Live USGS or local file upload
- Exposure-screening radius
- Satellite-catalogue mode and date range

The dashboard reports the active data source, total record count and latest available timestamp.
It then calculates and visualises:

- Total number of earthquake events
- Maximum recorded magnitude
- Median event depth
- Share of shallow events at 20 km or less
- Gutenberg–Richter b-value estimate
- Interactive earthquake-event map
- Daily event counts
- Magnitude through time
- Magnitude distribution
- Magnitude–depth relationship
- Statistical rolling event-rate anomaly screen
- Exploratory spatial clusters
- Missing values and duplicate records
- Coordinate and timestamp quality indicators
- Downloadable filtered catalogue data

The reporting layer is **near-real-time**, not second-by-second real-time. Results depend on the
publication schedule, completeness and interpretation of the upstream catalogue provider.

## Data modes

### 1. Reproducible demo mode

The bundled synthetic dataset allows the complete analytical workflow to run immediately without
registration, API keys or private data.

Synthetic records are explicitly labelled and must not be interpreted as observations of actual
earthquakes.

### 2. Live USGS mode

The application queries the official public USGS FDSN event service for recent events inside the
Türkiye bounding region.

The live source requires no private credential in the public application.

### 3. Local catalogue mode

Users can upload a CSV or Excel earthquake catalogue. The platform attempts to normalise common
column names and convert the input into the internal event schema.

Local files remain subject to the user's own data rights, quality controls and attribution duties.

## Catalogue analytics

The analytical layer includes:

- Event-schema standardisation
- UTC timestamp conversion
- Numeric magnitude and depth handling
- Coordinate-range validation
- Missing-value inspection
- Duplicate-event inspection
- Daily event aggregation
- Magnitude and depth summaries
- Shallow-event share calculation
- Gutenberg–Richter b-value estimation
- Rolling rate baselines and statistical anomaly flags
- DBSCAN-based spatial clustering
- Interactive map and time-series exploration

An anomaly flag means that the loaded catalogue differs statistically from its recent rolling
baseline. It is **not** a prediction of a future earthquake.

## Urban exposure screening

The platform can compare selected earthquake events with user-supplied population, facility or
infrastructure points.

The exposure workflow supports:

- CSV exposure-point inputs
- Latitude and longitude
- Optional name and category fields
- Optional analytical weight
- Adjustable screening radius
- Nearby-point counts
- Aggregated exposure-weight indicators
- Interactive exposure maps

This module is an exploratory proximity screen. It does not model structural vulnerability,
casualties, economic loss, building damage or official emergency impact.

## Satellite deformation workflow

The satellite module supports live Sentinel-1 catalogue discovery through the Copernicus Data
Space STAC service.

Current capabilities include:

- Sentinel-1 acquisition discovery
- Search by date and Türkiye bounding region
- Orbit-direction inspection
- Relative-orbit inspection
- Instrument-mode and polarisation metadata
- Same-orbit candidate-pair planning
- Uploaded processed displacement-point analysis
- Displacement summary statistics
- Interactive displacement maps

The web application does not calculate ground displacement directly from raw Sentinel-1 scenes.
Validated InSAR processing should be completed through specialist workflows such as SNAP, ISCE,
GMTSAR or MintPy before processed displacement points are uploaded.

## Data quality

The platform reports catalogue-level quality indicators, including:

- Record count
- Missing values
- Duplicate identifiers or timestamps
- Invalid coordinates
- Invalid magnitudes or depths
- Timestamp coverage
- Source labels
- Latest available record

These checks describe the loaded data structure. They do not independently validate sensor
calibration, magnitude accuracy, network completeness or the scientific interpretation supplied
by the original provider.

## Architecture

```text
USGS live catalogue ──────────────┐
AFAD-compatible local exports ────┤
User CSV / Excel catalogues ──────┼──> validation and normalisation
Reproducible demo data ───────────┤             │
Copernicus Sentinel-1 STAC ───────┘             ▼
                                      analytical research layer
                                                 │
                 ┌───────────────────────────────┼──────────────────────────────┐
                 ▼                               ▼                              ▼
          Streamlit dashboard              FastAPI service           CSV / BI / GIS exports
```

Core stack:

**Python · Pandas · NumPy · scikit-learn · Plotly · Streamlit · FastAPI ·
GitHub Actions · GitHub Pages · Zenodo**

## Quick start

```bash
git clone https://github.com/FaramarzKowsari/turkiye-seismic-intelligence-resilience-platform.git

cd turkiye-seismic-intelligence-resilience-platform

python -m venv .venv
```

Activate the environment:

```bash
# Windows
.venv\Scripts\activate

# macOS / Linux
source .venv/bin/activate
```

Install the project:

```bash
pip install -e ".[dev,app]"
```

Generate reproducible demo data:

```bash
python scripts/generate_demo.py
```

Run the dashboard:

```bash
streamlit run app/streamlit_app.py
```

Run the API:

```bash
uvicorn depremnabiz.api:app --reload
```

Run validation:

```bash
pytest
ruff check .
python scripts/release_audit.py
```

## Public access

**Interactive application**

https://depremnabiz-turkiye.streamlit.app

**Project website**

https://faramarzkowsari.github.io/turkiye-seismic-intelligence-resilience-platform/

**Source repository**

https://github.com/FaramarzKowsari/turkiye-seismic-intelligence-resilience-platform

## Data-source references

- AFAD Earthquake Department: https://deprem.afad.gov.tr/
- USGS Earthquake Catalog API: https://earthquake.usgs.gov/fdsnws/event/1/
- Copernicus Data Space STAC: https://stac.dataspace.copernicus.eu/v1/

External datasets remain subject to their original provider terms, licences, access limits and
attribution requirements.

---

<a id="türkçe"></a>

## Türkçe

### Proje hakkında

**DepremNabız AI**, deprem kataloglarını, uydu edinim metadatasını ve kullanıcı tarafından sağlanan
mekânsal girdileri şeffaf, denetlenebilir ve tekrar üretilebilir analitik ürünlere dönüştüren açık
kaynaklı bir araştırma yazılımıdır.

Platform aşağıdaki bileşenleri bir araya getirir:

- Türkiye için gerçek zamanlıya yakın deprem katalog analitiği
- Tekrar üretilebilir sentetik demo verileri
- Yerel CSV ve Excel katalog desteği
- Veri temizleme, şema normalizasyonu ve kalite raporlaması
- Zaman, büyüklük, derinlik ve mekân analizi
- Hareketli olay oranına dayalı anomali taraması
- Gutenberg–Richter b-değeri tahmini
- DBSCAN tabanlı mekânsal küme araştırması
- Yarıçap tabanlı kentsel maruziyet taraması
- Copernicus STAC üzerinden Sentinel-1 ürün keşfi
- Aynı yörüngeye ait uydu çifti planlaması
- İşlenmiş InSAR deplasman noktalarının incelenmesi
- Etkileşimli Streamlit raporlaması
- Salt okunur FastAPI hizmeti
- CSV, Excel, Parquet ve GeoJSON uyumlu çıktılar
- Otomatik testler, CI, sürüm doğrulaması ve DOI uyumlu metadata

## Canlı çevrim içi raporlama

Halka açık Streamlit uygulaması:

### [DepremNabız AI Uygulamasını Aç](https://depremnabiz-turkiye.streamlit.app)

**Live USGS** modu, resmî USGS Earthquake Catalog API üzerinden güncel deprem kayıtlarını alır ve
sorguyu Türkiye'nin coğrafi bölgesiyle sınırlar.

Kullanıcılar aşağıdaki seçenekleri değiştirebilir:

- 1 ile 90 gün arasında canlı veri aralığı
- Minimum deprem büyüklüğü
- Demo, Live USGS veya yerel dosya modu
- Maruziyet tarama yarıçapı
- Uydu kataloğu modu ve tarih aralığı

Dashboard, aktif veri kaynağını, toplam kayıt sayısını ve en güncel kayıt zamanını gösterir.
Ardından şu göstergeleri hesaplar ve görselleştirir:

- Toplam deprem sayısı
- En yüksek büyüklük
- Medyan derinlik
- 20 km ve altındaki sığ olayların oranı
- Gutenberg–Richter b-değeri tahmini
- Etkileşimli deprem haritası
- Günlük olay sayıları
- Zaman içinde büyüklük değişimi
- Büyüklük dağılımı
- Büyüklük ve derinlik ilişkisi
- Hareketli olay oranı anomali taraması
- Keşifsel mekânsal kümeler
- Eksik ve yinelenen kayıt kontrolleri
- Koordinat ve zaman damgası kalite göstergeleri
- Filtrelenmiş katalog için CSV indirme

Raporlama katmanı saniyelik gerçek zamanlı değildir; **gerçek zamanlıya yakın** çalışır. Sonuçların
güncelliği, üst veri sağlayıcısının yayın sıklığına ve katalog yapısına bağlıdır.

## Veri modları

### 1. Tekrar üretilebilir demo modu

Sentetik demo veri seti, kayıt veya API anahtarı gerektirmeden platformun bütün analitik
özelliklerinin incelenmesini sağlar.

Demo kayıtları açıkça sentetik olarak işaretlenmiştir ve gerçek deprem gözlemleri olarak
yorumlanmamalıdır.

### 2. Live USGS modu

Uygulama, resmî ve halka açık USGS FDSN hizmetinden Türkiye bölgesindeki güncel olayları sorgular.

Bu mod, halka açık uygulamada özel kullanıcı bilgisi gerektirmez.

### 3. Yerel katalog modu

Kullanıcılar CSV veya Excel deprem kataloglarını yükleyebilir. Platform yaygın sütun adlarını
normalleştirmeye ve verileri standart olay şemasına dönüştürmeye çalışır.

## Katalog analitiği

- Olay şeması standardizasyonu
- UTC zaman dönüşümü
- Büyüklük ve derinlik alanlarının normalizasyonu
- Koordinat aralığı kontrolü
- Eksik ve yinelenen kayıt analizi
- Günlük olay gruplaması
- Büyüklük ve derinlik özetleri
- Sığ olay oranı
- Gutenberg–Richter b-değeri
- Hareketli ortalama ve anomali işaretleri
- DBSCAN mekânsal kümeleri
- Harita ve zaman serisi görselleştirmeleri

Anomali etiketi, yüklenen katalogdaki istatistiksel bir sapmayı gösterir. Gelecekte gerçekleşecek
bir depremin tahmini değildir.

## Kentsel maruziyet taraması

Platform, seçilen deprem olaylarını kullanıcı tarafından sağlanan nüfus, tesis veya altyapı
noktalarıyla karşılaştırabilir.

Desteklenen özellikler:

- CSV maruziyet noktaları
- Enlem ve boylam
- İsteğe bağlı ad ve kategori
- İsteğe bağlı analitik ağırlık
- Ayarlanabilir tarama yarıçapı
- Yakındaki nokta sayısı
- Toplam maruziyet ağırlığı
- Etkileşimli maruziyet haritası

Bu bölüm bir yakınlık taramasıdır. Yapısal kırılganlık, can kaybı, bina hasarı veya resmî ekonomik
kayıp tahmini değildir.

## Uydu deformasyon iş akışı

Uydu modülü, Copernicus Data Space STAC üzerinden canlı Sentinel-1 katalog keşfini destekler.

Mevcut özellikler:

- Sentinel-1 edinim araması
- Tarih ve Türkiye sınır kutusuna göre filtreleme
- Yörünge yönü incelemesi
- Göreli yörünge bilgisi
- Mod ve polarizasyon metadatası
- Aynı yörünge çiftlerinin planlanması
- İşlenmiş deplasman noktalarının analizi
- Deplasman özet istatistikleri
- Etkileşimli deplasman haritası

Web uygulaması ham Sentinel-1 görüntülerinden doğrudan deplasman üretmez. Doğrulanmış InSAR
işlemleri SNAP, ISCE, GMTSAR veya MintPy gibi uzman araçlarla tamamlanmalıdır.

## Bilimsel ve etik sınırlar

Platform:

- Deprem tahmini yapmaz
- Erken uyarı hizmeti sunmaz
- Bina güvenliği sertifikası vermez
- Hasar, can kaybı veya ekonomik kayıp tahmini yapmaz
- Resmî kurum açıklamalarının yerine geçmez
- Acil durum müdahale sistemi olarak kullanılmamalıdır

Sonuçlar araştırma, eğitim, keşifsel analiz ve karar-destek prototiplemesi içindir.

---

## Repository structure

```text
app/                 Streamlit application
src/depremnabiz/     providers, pipeline, analytics, exposure, satellite and API
scripts/             demo generation, exports and release audit
data/demo/           clearly labelled synthetic examples
docs/                bilingual GitHub Pages website and technical documents
tests/               automated behavioural and metadata tests
.github/workflows/   CI, Pages, live snapshot and release validation
```

## Author

**Faramarz Kowsari** is an author, Software Engineer and AI researcher based in Istanbul.
Focusing on the intersection of technology, education, and personal growth, he has published
over 80 digital titles on international platforms. His areas of expertise span Artificial
Intelligence, prompt engineering, modern trading strategies (Smart Money Concepts & algorithmic
trading), as well as classical literature and mindfulness. In addition to writing, he develops
web-based educational tools and creates specialized instructional video content.

Official profiles:

[ORCID](https://orcid.org/0000-0003-1692-0453) ·
[Google Scholar](https://scholar.google.com/citations?user=G7tP5WMAAAAJ&hl=en) ·
[GitHub](https://github.com/FaramarzKowsari) ·
[LinkedIn](https://www.linkedin.com/in/faramarzkowsari) ·
[Google Books](https://play.google.com/store/search?q=Faramarz_Kowsari&c=books) ·
[Official Website](https://faramarzkowsari.github.io) ·
[Zenodo Records](https://zenodo.org/search?q=creators.orcid%3A%220000-0003-1692-0453%22&l=list&p=1&s=10&sort=bestmatch)

## Citation and preservation

<<<<<<< HEAD
**Version DOI:** [10.5281/zenodo.21797833](https://doi.org/10.5281/zenodo.21797833)
=======
Citation metadata is provided in [`CITATION.cff`](CITATION.cff).

Until the first GitHub release is archived by Zenodo, cite the software as:

```text
Kowsari, Faramarz. Türkiye Seismic Intelligence & Resilience Platform:
DepremNabız AI, Version 1.0.0. GitHub, 2026.
https://github.com/FaramarzKowsari/turkiye-seismic-intelligence-resilience-platform
```

After Zenodo creates the first version DOI, update the citation metadata with:
>>>>>>> 476e000d9227549fc3dcd20b064e4a5556ddb826

Kowsari, Faramarz. **Türkiye Seismic Intelligence & Resilience Platform (DepremNabız AI), version 1.0.0**. Zenodo. [10.5281/zenodo.21797833](https://doi.org/10.5281/zenodo.21797833)

The repository badge should remain linked to the Concept DOI after the first DOI is minted.

## Licence

Source code is released under the **MIT License**.

External data, catalogues and satellite products remain subject to the licences, access conditions,
usage limits and attribution requirements of their original providers.
