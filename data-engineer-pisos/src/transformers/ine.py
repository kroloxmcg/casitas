import json
from datetime import datetime
from pathlib import Path

import polars as pl

from src.config import PROJECT_ROOT


def transform_ine(raw_path: Path) -> Path:
    """Normalize INE IPV data into a structured Parquet file."""
    raw = json.loads(raw_path.read_text())

    records = []
    for category, entries in raw.items():
        for entry in entries:
            records.append(
                {
                    "category": category,
                    "period": entry.get("periodo", ""),
                    "value": entry.get("valor"),
                }
            )

    df = pl.DataFrame(records)
    df = df.with_columns(pl.col("value").cast(pl.Float64, strict=False))

    output = PROJECT_ROOT / "data" / "processed" / f"ine_ipv_{datetime.now():%Y%m%d}.parquet"
    output.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(output)
    return output
