import asyncio
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(help="pisos-etl: ETL pipeline for Spanish real estate data")
console = Console()


@app.command()
def extract(
    source: str = typer.Argument(..., help="Source to extract: idealista, ine, serpavi"),
    center: str = typer.Option("40.4168,-3.7038", help="Lat,Lon center (idealista)"),
    distance: int = typer.Option(15000, help="Search radius in meters (idealista)"),
    operation: str = typer.Option("sale", help="sale or rent (idealista)"),
    max_pages: int = typer.Option(2, help="Max pages to fetch (idealista)"),
):
    """Extract raw data from a source."""
    from src.extractors import IdealistaExtractor, INEExtractor, SERPAVIExtractor

    extractors = {
        "idealista": lambda: IdealistaExtractor().extract(
            center=center, distance=distance, operation=operation, max_pages=max_pages
        ),
        "ine": lambda: INEExtractor().extract(),
        "serpavi": lambda: SERPAVIExtractor().extract(),
    }

    if source not in extractors:
        console.print(f"[red]Unknown source: {source}. Use: {', '.join(extractors)}[/red]")
        raise typer.Exit(1)

    console.print(f"[cyan]Extracting from {source}...[/cyan]")
    output = asyncio.run(extractors[source]())
    console.print(f"[green]Saved to {output}[/green]")


@app.command()
def transform(
    source: str = typer.Argument(..., help="Source to transform: idealista, ine"),
    raw_file: Path = typer.Argument(..., help="Path to raw JSON file"),
):
    """Transform raw data into structured Parquet."""
    from src.transformers import transform_idealista, transform_ine, transform_serpavi

    transformers = {
        "idealista": transform_idealista,
        "ine": transform_ine,
        "serpavi": transform_serpavi,
    }

    if source not in transformers:
        console.print(f"[red]Unknown source: {source}. Use: {', '.join(transformers)}[/red]")
        raise typer.Exit(1)

    console.print(f"[cyan]Transforming {source} data...[/cyan]")
    output = transformers[source](raw_file)
    console.print(f"[green]Saved to {output}[/green]")


@app.command()
def load(
    parquet_file: Path = typer.Argument(..., help="Path to Parquet file"),
    table_name: str = typer.Argument(..., help="Target table name in DuckDB"),
):
    """Load a Parquet file into DuckDB."""
    from src.loaders import DuckDBLoader

    loader = DuckDBLoader()
    console.print(f"[cyan]Loading into {table_name}...[/cyan]")
    count = loader.load_parquet(parquet_file, table_name)
    console.print(f"[green]Loaded {count} rows into {table_name}[/green]")


@app.command()
def query(sql: str = typer.Argument(..., help="SQL query to run")):
    """Run a SQL query against DuckDB."""
    from src.loaders import DuckDBLoader

    loader = DuckDBLoader()
    results = loader.query(sql)

    if not results:
        console.print("[yellow]No results[/yellow]")
        return

    table = Table()
    for col in results[0]:
        table.add_column(col)
    for row in results[:50]:
        table.add_row(*[str(v) for v in row.values()])
    console.print(table)


@app.command()
def pipeline(
    source: str = typer.Argument("idealista", help="Source to run full pipeline for"),
):
    """Run the full ETL pipeline: extract -> transform -> load."""
    from src.extractors import IdealistaExtractor, INEExtractor, SERPAVIExtractor
    from src.loaders import DuckDBLoader
    from src.transformers import transform_idealista, transform_ine, transform_serpavi

    pipelines = {
        "idealista": (IdealistaExtractor, transform_idealista, "listings"),
        "ine": (INEExtractor, transform_ine, "ipv"),
        "serpavi": (SERPAVIExtractor, transform_serpavi, "rentals"),
    }

    if source not in pipelines:
        console.print(f"[red]Unknown pipeline: {source}. Use: {', '.join(pipelines)}[/red]")
        raise typer.Exit(1)

    extractor_cls, transformer, table_name = pipelines[source]

    console.print(f"[cyan]1/3 Extracting {source}...[/cyan]")
    raw_path = asyncio.run(extractor_cls().extract())
    console.print(f"  -> {raw_path}")

    console.print(f"[cyan]2/3 Transforming...[/cyan]")
    parquet_path = transformer(raw_path)
    console.print(f"  -> {parquet_path}")

    console.print(f"[cyan]3/3 Loading into DuckDB ({table_name})...[/cyan]")
    loader = DuckDBLoader()
    count = loader.load_parquet(parquet_path, table_name)
    console.print(f"[green]Pipeline complete: {count} rows in '{table_name}'[/green]")


if __name__ == "__main__":
    app()
