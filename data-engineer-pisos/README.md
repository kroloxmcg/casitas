# pisos-etl

ETL pipeline for Spanish real estate data. Extracts listings, price indices and rental references from multiple sources, transforms them into structured Parquet files, and loads them into DuckDB for analysis.

## Data sources

| Source | Data | Granularity | Auth required |
|---|---|---|---|
| **Idealista API** | Individual property listings (price, m², rooms, location, ...) | Per listing | Yes — [request access](https://developers.idealista.com/access-request) |
| **INE (IPV)** | Housing Price Index, quarterly, national | National / quarterly | No |
| **SERPAVI** | Official rental prices (median, P25, P75), surface, num properties (2011-2024) | CCAA, province, municipality, district | No (manual Excel download from [MIVAU](https://www.mivau.gob.es/vivienda/alquila-bien-es-tu-derecho/serpavi)) |

### SERPAVI metrics per year

- Rent per m² (median, P25, P75) — collective and single-family housing
- Monthly rent total (median, P25, P75)
- Surface m² (median, P25, P75)
- Number of properties

## Setup

```bash
cp .env.example .env    # add your Idealista API credentials
pip install -e ".[dev]"
```

For SERPAVI, download the Excel from the [MIVAU portal](https://www.mivau.gob.es/vivienda/alquila-bien-es-tu-derecho/serpavi) ("BD Sistema Estatal Indices de Alquiler de Vivienda") and place it at `data/raw/serpavi_2011_2024.xlsx`.

## Usage

### Full pipeline (extract -> transform -> load)

```bash
# INE — works out of the box, no API key needed
make pipeline-ine

# SERPAVI — requires the Excel in data/raw/
make pipeline-serpavi

# Idealista — requires API credentials in .env
make pipeline-idealista
```

### Step by step

```bash
# Extract
python -m src.cli extract ine
python -m src.cli extract serpavi
python -m src.cli extract idealista --center "40.4168,-3.7038" --distance 15000

# Transform
python -m src.cli transform ine data/raw/ine_*.json
python -m src.cli transform serpavi data/raw/serpavi_*_raw.json
python -m src.cli transform idealista data/raw/idealista_*.json

# Load into DuckDB
python -m src.cli load data/processed/ine_ipv_*.parquet ipv
python -m src.cli load data/processed/serpavi_*.parquet rentals
python -m src.cli load data/processed/idealista_*.parquet listings

# Query
python -m src.cli query "SELECT district, avg(price) FROM listings GROUP BY district"
```

### Example queries

```sql
-- Rental evolution in Madrid (municipality level)
SELECT name, year, monthly_rent_median_collective, rent_m2_median_collective
FROM rentals WHERE level='municipio' AND name='Madrid' ORDER BY year;

-- Most expensive Madrid districts in 2024
SELECT code, monthly_rent_median_collective, rent_m2_median_collective
FROM rentals WHERE level='distrito' AND name='Madrid' AND year=2024
ORDER BY rent_m2_median_collective DESC;

-- IPV national index evolution
SELECT category, year, quarter, value FROM ipv ORDER BY category, year, quarter;
```

Pre-built queries also available in `sql/analysis.sql`.

## Project structure

```
data-engineer-pisos/
├── config/sources.toml       # source URLs and parameters
├── data/
│   ├── raw/                  # extracted JSON + Excel (gitignored)
│   ├── staging/              # intermediate files
│   └── processed/            # clean Parquet files (gitignored)
├── sql/analysis.sql          # ready-to-run DuckDB queries
├── src/
│   ├── cli.py                # typer CLI (extract, transform, load, pipeline, query)
│   ├── config.py             # pydantic-settings
│   ├── extractors/           # one per data source (idealista, ine, serpavi)
│   ├── transformers/         # raw JSON -> normalized Parquet (polars)
│   └── loaders/              # Parquet -> DuckDB
└── tests/
```

## Stack

- **Python 3.11+** with httpx, polars, pydantic
- **DuckDB** as the analytical warehouse
- **Parquet** as the intermediate format
- **typer + rich** for the CLI
