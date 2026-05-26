import json
import re
from datetime import datetime
from pathlib import Path

import polars as pl

from src.config import PROJECT_ROOT

METRIC_LABELS = {
    "BI_ALVHEPCO_TVC": "num_properties_collective",
    "BI_ALVHEPCO_TVU": "num_properties_single_family",
    "ALQM2_LV_M_VC": "rent_m2_median_collective",
    "ALQM2_LV_25_VC": "rent_m2_p25_collective",
    "ALQM2_LV_75_VC": "rent_m2_p75_collective",
    "ALQM2_LV_M_VU": "rent_m2_median_single_family",
    "ALQM2_LV_25_VU": "rent_m2_p25_single_family",
    "ALQM2_LV_75_VU": "rent_m2_p75_single_family",
    "ALQTBID12_M_VC": "monthly_rent_median_collective",
    "ALQTBID12_25_VC": "monthly_rent_p25_collective",
    "ALQTBID12_75_VC": "monthly_rent_p75_collective",
    "ALQTBID12_M_VU": "monthly_rent_median_single_family",
    "ALQTBID12_25_VU": "monthly_rent_p25_single_family",
    "ALQTBID12_75_VU": "monthly_rent_p75_single_family",
    "SLVM2_M_VC": "surface_m2_median_collective",
    "SLVM2_25_VC": "surface_m2_p25_collective",
    "SLVM2_75_VC": "surface_m2_p75_collective",
    "SLVM2_M_VU": "surface_m2_median_single_family",
    "SLVM2_25_VU": "surface_m2_p25_single_family",
    "SLVM2_75_VU": "surface_m2_p75_single_family",
}

YEAR_SUFFIX_RE = re.compile(r"^(.+)_(\d{2})$")


def _parse_column(col: str) -> tuple[str, int] | None:
    m = YEAR_SUFFIX_RE.match(col)
    if not m:
        return None
    metric_raw, year_suffix = m.group(1), int(m.group(2))
    year = 2000 + year_suffix
    if metric_raw in METRIC_LABELS:
        return METRIC_LABELS[metric_raw], year
    return None


def _unpivot_level(rows: list[dict], code_col: str, name_col: str, level: str) -> list[dict]:
    records = []
    for row in rows:
        code = str(row.get(code_col, ""))
        name = row.get(name_col, "")

        year_data: dict[int, dict] = {}
        for col, val in row.items():
            parsed = _parse_column(col)
            if parsed is None:
                continue
            metric, year = parsed
            if year not in year_data:
                year_data[year] = {"level": level, "code": code, "name": name, "year": year}
            year_data[year][metric] = val

        records.extend(year_data.values())
    return records


LEVEL_CONFIG = {
    "ccaa": ("CCAA", "LITCCAA"),
    "provincia": ("CPRO", "LITPRO"),
    "municipio": ("CUMUN", "NMUN"),
    "distrito": ("CUDIS", "LITMUN"),
}


def transform_serpavi(raw_path: Path, levels: list[str] | None = None) -> Path:
    """Unpivot wide-format SERPAVI data into normalized long-format Parquet."""
    raw = json.loads(raw_path.read_text())

    if levels is None:
        levels = list(raw.keys())

    all_records = []
    for level in levels:
        if level not in raw:
            continue
        code_col, name_col = LEVEL_CONFIG[level]
        rows = raw[level]["rows"]
        all_records.extend(_unpivot_level(rows, code_col, name_col, level))

    df = pl.DataFrame(all_records)

    float_cols = [c for c in df.columns if c not in ("level", "code", "name", "year")]
    df = df.with_columns([pl.col(c).cast(pl.Float64, strict=False) for c in float_cols])

    output = PROJECT_ROOT / "data" / "processed" / f"serpavi_{datetime.now():%Y%m%d}.parquet"
    output.parent.mkdir(parents=True, exist_ok=True)
    df.write_parquet(output)
    return output
