import json
from pathlib import Path

from .base import BaseExtractor

DEFAULT_PATH = "data/raw/serpavi_2011_2024.xlsx"


class SERPAVIExtractor(BaseExtractor):
    """Extract rental price reference data from SERPAVI (Ministerio de Vivienda).

    SERPAVI provides a single Excel download with wide-format data (metrics x years
    as columns). This extractor reads specific sheets and outputs raw JSON per sheet.
    """

    name = "serpavi"

    SHEETS = {
        "CCAA": {"level": "ccaa"},
        "Provincias": {"level": "provincia"},
        "Municipios": {"level": "municipio"},
        "Distritos": {"level": "distrito"},
    }

    async def extract(self, *, excel_path: str = DEFAULT_PATH, **kwargs) -> Path:
        import pandas as pd

        from src.config import PROJECT_ROOT

        resolved = Path(excel_path)
        if not resolved.is_absolute():
            resolved = PROJECT_ROOT / resolved

        if not resolved.exists():
            output = self.output_path("instructions")
            output.write_text(json.dumps({
                "error": "File not found",
                "expected_path": str(resolved),
                "download_from": "https://www.mivau.gob.es/vivienda/alquila-bien-es-tu-derecho/serpavi",
            }, indent=2))
            return output

        all_data = {}
        for sheet_name, meta in self.SHEETS.items():
            df = pd.read_excel(resolved, sheet_name=sheet_name, engine="openpyxl")
            all_data[meta["level"]] = {
                "columns": list(df.columns),
                "rows": df.to_dict(orient="records"),
                "count": len(df),
            }

        output = self.output_path("raw")
        output.write_text(
            json.dumps(all_data, ensure_ascii=False, default=str),
        )
        return output
