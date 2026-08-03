from __future__ import annotations

from pathlib import Path

import pandas as pd
import typer

from depremnabiz.analytics import summary
from depremnabiz.exports import write_exports
from depremnabiz.pipeline import clean_events
from depremnabiz.providers.usgs import fetch_events

app = typer.Typer(help="DepremNabız AI command line interface.")


@app.command()
def live(days: int = 7, min_magnitude: float = 2.0, output: Path = Path("outputs/live")) -> None:
    frame = clean_events(fetch_events(days=days, min_magnitude=min_magnitude))
    paths = write_exports(frame, output)
    typer.echo(summary(frame))
    typer.echo(paths)


@app.command()
def export(input_path: Path, output: Path = Path("outputs/local")) -> None:
    frame = pd.read_csv(input_path)
    paths = write_exports(clean_events(frame), output)
    typer.echo(paths)


if __name__ == "__main__":
    app()
