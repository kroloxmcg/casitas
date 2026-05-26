# pisos-etl

ETL pipeline for Spanish real estate data. Extracts listings and price indices from multiple sources, transforms them into structured Parquet files, and loads them into DuckDB for analysis.

## Data sources

| Source | Data | Auth required |
|---|---|---|
| **Idealista API** | Individual property listings (price, m², rooms, location, ...) | Yes — [request access](https://developers.idealista.com/access-request) |
| **INE (IPV)** | Housing Price Index, quarterly, by region | No |
| **SERPAVI** | Official rental price references by postal code (2011-2024) | No (manual Excel download) |

## Setup

```bash
cp .env.example .env    # add your Idealista API credentials
pip install -e ".[dev]"
```

## Usage

### Full pipeline (extract → transform → load)

```bash
# INE — works out of the box, no API key needed
make pipeline-ine

# Idealista — requires API credentials in .env
make pipeline-idealista
```

### Step by step

```bash
# Extract
python -m src.cli extract ine
python -m src.cli extract idealista --center "40.4168,-3.7038" --distance 15000

# Transform
python -m src.cli transform ine data/raw/ine_*.json
python -m src.cli transform idealista data/raw/idealista_*.json

# Load into DuckDB
python -m src.cli load data/processed/ine_ipv_*.parquet ipv
python -m src.cli load data/processed/idealista_*.parquet listings

# Query
python -m src.cli query "SELECT district, avg(price) FROM listings GROUP BY district"
```

### Analysis queries

Pre-built queries in `sql/analysis.sql`:
- Average price per m² by district
- Price distribution percentiles by operation type
- Cheapest listings per m² (outlier detection)
- IPV index evolution

## Project structure

```
data-engineer-pisos/
├── config/sources.toml       # source URLs and parameters
├── data/
│   ├── raw/                  # extracted JSON (gitignored)
│   ├── staging/              # intermediate files
│   └── processed/            # clean Parquet files (gitignored)
├── sql/analysis.sql          # ready-to-run DuckDB queries
├── src/
│   ├── cli.py                # typer CLI
│   ├── config.py             # pydantic-settings
│   ├── extractors/           # one per data source
│   ├── transformers/         # raw JSON → Parquet (polars)
│   └── loaders/              # Parquet → DuckDB
└── tests/
```

## Stack

- **Python 3.11+** with httpx, polars, pydantic
- **DuckDB** as the analytical warehouse
- **Parquet** as the intermediate format
- **typer + rich** for the CLI
