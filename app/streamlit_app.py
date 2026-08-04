from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from depremnabiz.analytics import (
    daily_counts,
    estimate_b_value,
    rolling_rate_anomalies,
    spatial_clusters,
    summary,
)
from depremnabiz.exposure import screen_exposure
from depremnabiz.pipeline import clean_events, normalise_events, quality_report
from depremnabiz.providers.copernicus import search_sentinel1
from depremnabiz.providers.usgs import fetch_events
from depremnabiz.satellite import build_pair_plan, summarise_displacement

ROOT = Path(__file__).resolve().parents[1]
DEMO_EVENTS = ROOT / "data" / "demo" / "earthquakes.csv"
DEMO_EXPOSURE = ROOT / "data" / "demo" / "exposure_points.csv"
DEMO_SENTINEL = ROOT / "data" / "demo" / "sentinel_catalog.csv"

st.set_page_config(
    page_title="DepremNabız AI",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("DepremNabız AI")
st.caption("Türkiye Seismic Intelligence & Resilience Platform")
st.warning(
    "Research analytics only. This application does not predict earthquakes, issue early warnings "
    "or replace official authorities."
)

with st.sidebar:
    st.header("Data source")
    mode = st.radio("Mode", ["Demo data", "Live USGS", "Upload local file"])
    days = st.slider("Live lookback (days)", 1, 90, 30)
    min_magnitude = st.slider("Minimum magnitude", 0.0, 6.0, 1.5, 0.1)
    uploaded = None
    if mode == "Upload local file":
        uploaded = st.file_uploader("CSV or Excel earthquake catalogue", type=["csv", "xlsx", "xls"])

@st.cache_data(ttl=900, show_spinner=False)
def cached_usgs(live_days: int, minimum: float) -> pd.DataFrame:
    return fetch_events(days=live_days, min_magnitude=minimum)

source_label = "Synthetic demo data"
try:
    if mode == "Live USGS":
        with st.spinner("Retrieving official USGS records..."):
            frame = clean_events(cached_usgs(days, min_magnitude))
        source_label = "Official USGS Earthquake Catalog API"
    elif mode == "Upload local file" and uploaded is not None:
        raw = pd.read_excel(uploaded) if uploaded.name.lower().endswith((".xlsx", ".xls")) else pd.read_csv(uploaded)
        frame = clean_events(normalise_events(raw, source="USER_UPLOAD"))
        source_label = "User-supplied local catalogue"
    else:
        frame = clean_events(pd.read_csv(DEMO_EVENTS))
except Exception as exc:
    st.error(f"The selected source could not be loaded: {exc}")
    frame = clean_events(pd.read_csv(DEMO_EVENTS))
    source_label = "Synthetic demo fallback"

st.success(
    f"Source: {source_label} · records: {len(frame):,} · "
    f"latest: {frame['time_utc'].max() if not frame.empty else 'n/a'}"
)

metrics = summary(frame)
quality = quality_report(frame)
b_value = estimate_b_value(frame, completeness_magnitude=max(1.0, min_magnitude))
columns = st.columns(5)
columns[0].metric("Events", f"{metrics['events']:,}")
columns[1].metric("Maximum magnitude", "n/a" if metrics["max_magnitude"] is None else f"{metrics['max_magnitude']:.1f}")
columns[2].metric("Median depth", "n/a" if metrics["median_depth_km"] is None else f"{metrics['median_depth_km']:.1f} km")
columns[3].metric("Shallow share ≤20 km", "n/a" if metrics["shallow_share"] is None else f"{100 * metrics['shallow_share']:.1f}%")
columns[4].metric("b-value estimate", "n/a" if b_value["b_value"] is None else f"{b_value['b_value']:.2f}")

catalogue_tab, quality_tab, exposure_tab, satellite_tab, methods_tab = st.tabs(
    ["Catalogue analytics", "Data quality", "Urban exposure", "Satellite deformation", "Methods & limits"]
)

with catalogue_tab:
    if not frame.empty:
        clustered = spatial_clusters(frame)
        map_figure = px.scatter_map(
            clustered,
            lat="latitude",
            lon="longitude",
            size=clustered["magnitude"].fillna(0).clip(lower=0.4) ** 2,
            color="magnitude",
            hover_name="place",
            hover_data=["time_utc", "depth_km", "source", "cluster"],
            zoom=4,
            height=570,
            map_style="open-street-map",
            color_continuous_scale="Turbo",
            title="Earthquake-event map",
        )
        st.plotly_chart(map_figure, width="stretch")

        left, right = st.columns(2)
        daily = daily_counts(frame)
        left.plotly_chart(
            px.bar(daily, x="date", y="event_count", title="Daily event counts"),
            width="stretch",
        )
        right.plotly_chart(
            px.scatter(
                frame,
                x="time_utc",
                y="magnitude",
                color="depth_km",
                size=frame["magnitude"].fillna(0).clip(lower=0.3) ** 2,
                title="Magnitude through time",
            ),
            width="stretch",
        )

        left, right = st.columns(2)
        left.plotly_chart(
            px.histogram(frame, x="magnitude", nbins=30, title="Magnitude distribution"),
            width="stretch",
        )
        right.plotly_chart(
            px.scatter(
                frame,
                x="magnitude",
                y="depth_km",
                color="magnitude",
                title="Magnitude–depth relationship",
            ).update_yaxes(autorange="reversed"),
            width="stretch",
        )

        anomaly = rolling_rate_anomalies(frame)
        anomaly_figure = go.Figure()
        anomaly_figure.add_scatter(x=anomaly["date"], y=anomaly["event_count"], name="Daily count")
        anomaly_figure.add_scatter(x=anomaly["date"], y=anomaly["rolling_mean"], name="Rolling baseline")
        flagged = anomaly[anomaly["anomaly"]]
        anomaly_figure.add_scatter(
            x=flagged["date"],
            y=flagged["event_count"],
            mode="markers",
            marker={"size": 12, "symbol": "x"},
            name="Screened anomaly",
        )
        anomaly_figure.update_layout(title="Rolling event-rate anomaly screen")
        st.plotly_chart(anomaly_figure, width="stretch")

        export_frame = frame.copy()
        st.download_button(
            "Download filtered catalogue CSV",
            export_frame.to_csv(index=False).encode("utf-8"),
            file_name="depremnabiz_catalogue.csv",
            mime="text/csv",
            width="stretch",
        )
    else:
        st.info("No events are available for the selected filters.")

with quality_tab:
    quality_frame = pd.DataFrame(
        [{"metric": key, "value": value} for key, value in quality.items()]
    )
    st.dataframe(quality_frame, width="stretch", hide_index=True)
    st.write(
        "Quality metrics describe the loaded catalogue only. They do not validate magnitude "
        "accuracy, network completeness or provider interpretation."
    )

with exposure_tab:
    st.subheader("Radius-based exposure screening")
    st.caption("This is an exposure proxy, not a damage, casualty or loss estimate.")
    exposure_upload = st.file_uploader(
        "Exposure points CSV: latitude, longitude, optional name/category/weight",
        type=["csv"],
        key="exposure",
    )
    exposure_points = pd.read_csv(exposure_upload) if exposure_upload else pd.read_csv(DEMO_EXPOSURE)
    exposure_label = "User-supplied" if exposure_upload else "Synthetic demo"
    radius = st.slider("Screening radius (km)", 5, 150, 50, 5)
    selected_events = frame.nlargest(min(50, len(frame)), "magnitude") if not frame.empty else frame
    try:
        screened = screen_exposure(selected_events, exposure_points, radius_km=radius)
        st.info(f"Exposure source: {exposure_label}; points: {len(exposure_points):,}")
        st.dataframe(screened.sort_values("exposure_weight", ascending=False), width="stretch", hide_index=True)
        st.plotly_chart(
            px.scatter_map(
                exposure_points,
                lat="latitude",
                lon="longitude",
                size=exposure_points.get("weight", pd.Series(1, index=exposure_points.index)),
                color=exposure_points.get("category", pd.Series("point", index=exposure_points.index)),
                hover_name=exposure_points.get("name", pd.Series("exposure point", index=exposure_points.index)),
                zoom=4,
                height=500,
                map_style="open-street-map",
                title="Exposure points",
            ),
            width="stretch",
        )
    except Exception as exc:
        st.error(str(exc))

with satellite_tab:
    st.subheader("Sentinel-1 discovery and deformation-product exploration")
    st.caption(
        "The live catalogue identifies acquisitions for downstream InSAR processing. It does not "
        "derive displacement from raw Sentinel-1 scenes inside the web app."
    )
    satellite_mode = st.radio("Satellite catalogue", ["Demo catalogue", "Live Copernicus STAC"], horizontal=True)
    if satellite_mode == "Live Copernicus STAC":
        date_end = date.today()
        date_start = date_end - timedelta(days=60)
        start = st.date_input("Start date", date_start)
        end = st.date_input("End date", date_end)
        if st.button("Search Sentinel-1 acquisitions", width="stretch"):
            try:
                satellite_catalogue = search_sentinel1((25.0, 35.5, 46.5, 43.0), start, end)
                st.session_state["satellite_catalogue"] = satellite_catalogue
            except Exception as exc:
                st.error(f"Copernicus STAC search failed: {exc}")
        satellite_catalogue = st.session_state.get("satellite_catalogue", pd.DataFrame())
    else:
        satellite_catalogue = pd.read_csv(DEMO_SENTINEL)
        satellite_catalogue["datetime"] = pd.to_datetime(satellite_catalogue["datetime"], utc=True)

    st.dataframe(satellite_catalogue, width="stretch", hide_index=True)
    pair_plan = build_pair_plan(satellite_catalogue)
    st.write("Candidate same-orbit pairs")
    st.dataframe(pair_plan, width="stretch", hide_index=True)

    displacement_upload = st.file_uploader(
        "Optional processed InSAR points CSV: latitude, longitude, displacement_mm",
        type=["csv"],
        key="displacement",
    )
    if displacement_upload:
        displacement = pd.read_csv(displacement_upload)
        try:
            displacement_summary = summarise_displacement(displacement)
            st.json(displacement_summary)
            st.plotly_chart(
                px.scatter_map(
                    displacement,
                    lat="latitude",
                    lon="longitude",
                    color="displacement_mm",
                    size=displacement["displacement_mm"].abs().clip(lower=0.5),
                    color_continuous_scale="RdBu_r",
                    map_style="open-street-map",
                    zoom=6,
                    height=550,
                    title="Uploaded displacement points",
                ),
                width="stretch",
            )
        except Exception as exc:
            st.error(str(exc))

with methods_tab:
    st.markdown(
        """
### Interpretation rules

- **Anomaly** means a statistical deviation in the loaded catalogue,
  not a forecast of a future event.
- **b-value** depends on magnitude completeness and catalogue selection.
- **Clusters** are exploratory groups controlled by DBSCAN parameters.
- **Exposure** counts nearby user-supplied points; it is not vulnerability,
  damage or loss.
- **Satellite discovery** builds acquisition manifests. Deformation processing
  belongs in a validated SNAP, ISCE, GMTSAR or MintPy workflow.

### Scientific and operational limits

This platform is designed for research, education, exploratory analysis and
decision-support prototyping. It does not predict earthquakes, issue official
early warnings, certify buildings or estimate official casualties and losses.
"""
    )


# ---------------------------------------------------------------------------
# Project source
# ---------------------------------------------------------------------------

st.divider()
st.subheader("Project source / Proje kaynak kodu / Código fuente del proyecto")

source_en, source_tr, source_es = st.tabs(["English", "Türkçe", "Español"])

with source_en:
    st.markdown(
        """
This Streamlit application is the public interactive interface of the
**Türkiye Seismic Intelligence & Resilience Platform — DepremNabız AI**.

The complete source code, data pipeline, analytical modules, automated tests,
GitHub Actions workflows, documentation and release metadata are maintained in
the public GitHub repository of **Faramarz Kowsari**.

**Source repository**

https://github.com/FaramarzKowsari/\
turkiye-seismic-intelligence-resilience-platform
"""
    )

with source_tr:
    st.markdown(
        """
Bu Streamlit uygulaması, **Türkiye Seismic Intelligence & Resilience Platform —
DepremNabız AI** projesinin halka açık etkileşimli arayüzüdür.

Projenin kaynak kodu, veri hattı, analitik modülleri, otomatik testleri,
GitHub Actions iş akışları, dokümantasyonu ve sürüm metadatası
**Faramarz Kowsari** GitHub hesabındaki halka açık depoda yayımlanmaktadır.

**Kaynak kod deposu**

https://github.com/FaramarzKowsari/\
turkiye-seismic-intelligence-resilience-platform
"""
    )

with source_es:
    st.markdown(
        """
Esta aplicación de Streamlit es la interfaz pública e interactiva del
**Türkiye Seismic Intelligence & Resilience Platform — DepremNabız AI**.

El código fuente completo, la canalización de datos, los módulos analíticos,
las pruebas automatizadas, los flujos de trabajo de GitHub Actions,
la documentación y los metadatos de las versiones se mantienen en el
repositorio público de GitHub de **Faramarz Kowsari**.

**Repositorio del código fuente**

https://github.com/FaramarzKowsari/\
turkiye-seismic-intelligence-resilience-platform
"""
    )

source_buttons = st.columns(2)

source_buttons[0].link_button(
    "Open GitHub source repository",
    (
        "https://github.com/FaramarzKowsari/"
        "turkiye-seismic-intelligence-resilience-platform"
    ),
    width="stretch",
)

source_buttons[1].link_button(
    "Open project website",
    (
        "https://faramarzkowsari.github.io/"
        "turkiye-seismic-intelligence-resilience-platform/"
    ),
    width="stretch",
)


# ---------------------------------------------------------------------------
# Author
# ---------------------------------------------------------------------------

st.divider()
st.subheader("About the author / Yazar hakkında / Sobre el autor")

photo_column, biography_column = st.columns([1, 3])

with photo_column:
    st.image(
        "https://avatars.githubusercontent.com/u/105053743?v=4&s=512",
        caption="Faramarz Kowsari",
        width=190,
    )

with biography_column:
    bio_en, bio_tr, bio_es = st.tabs(["English", "Türkçe", "Español"])

    with bio_en:
        st.markdown(
            """
### Faramarz Kowsari

**Author · Software Engineer · AI Researcher**

Faramarz Kowsari is an author, Software Engineer and AI researcher based in
Istanbul. Focusing on the intersection of technology, education, and personal
growth, he has published over 80 digital titles on international platforms.

His areas of expertise span Artificial Intelligence, prompt engineering,
modern trading strategies — including Smart Money Concepts and algorithmic
trading — as well as classical literature and mindfulness.

In addition to writing, he develops web-based educational tools and creates
specialized instructional video content.
"""
        )

    with bio_tr:
        st.markdown(
            """
### Faramarz Kowsari

**Yazar · Yazılım Mühendisi · Yapay Zekâ Araştırmacısı**

Faramarz Kowsari, İstanbul merkezli bir yazar, Yazılım Mühendisi ve
Yapay Zekâ araştırmacısıdır. Teknoloji, eğitim ve kişisel gelişimin kesişimine
odaklanarak uluslararası platformlarda 80'den fazla dijital eser yayımlamıştır.

Uzmanlık alanları Yapay Zekâ, prompt mühendisliği, modern işlem stratejileri —
Smart Money Concepts ve algoritmik işlem dâhil — klasik edebiyat ve farkındalık
çalışmalarını kapsar.

Yazarlığın yanı sıra web tabanlı eğitim araçları geliştirir ve uzmanlaşmış
öğretici video içerikleri üretir.
"""
        )

    with bio_es:
        st.markdown(
            """
### Faramarz Kowsari

**Autor · Ingeniero de Software · Investigador en Inteligencia Artificial**

Faramarz Kowsari es autor, ingeniero de software e investigador en Inteligencia
Artificial con base en Estambul. Centrado en la intersección entre tecnología,
educación y desarrollo personal, ha publicado más de 80 títulos digitales en
plataformas internacionales.

Sus áreas de especialización abarcan la Inteligencia Artificial, la ingeniería
de prompts, las estrategias modernas de trading —incluidos Smart Money Concepts
y el trading algorítmico—, así como la literatura clásica y la atención plena.

Además de escribir, desarrolla herramientas educativas basadas en la web y crea
contenido audiovisual formativo especializado.
"""
        )


st.markdown(
    """
#### Official profiles / Resmî profiller / Perfiles oficiales

[ORCID](https://orcid.org/0000-0003-1692-0453) ·
[Google Scholar](https://scholar.google.com/citations?user=G7tP5WMAAAAJ&hl=en) ·
[GitHub](https://github.com/FaramarzKowsari) ·
[LinkedIn](https://www.linkedin.com/in/faramarzkowsari) ·
[Google Books](https://play.google.com/store/search?q=Faramarz_Kowsari&c=books) ·
[Official Website](https://faramarzkowsari.github.io) ·
[Zenodo Records](https://zenodo.org/search?q=creators.orcid%3A%220000-0003-1692-0453%22)
"""
)

st.caption(
    "Türkiye Seismic Intelligence & Resilience Platform · "
    "DepremNabız AI · Created and maintained by Faramarz Kowsari"
)
