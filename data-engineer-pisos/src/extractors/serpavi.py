import json
from pathlib import Path

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from .base import BaseExtractor

SERPAVI_BASE = "https://www.mivau.gob.es"
DOWNLOAD_HINT = (
    "SERPAVI data must be downloaded manually from:\n"
    "https://www.mivau.gob.es/vivienda/alquila-bien-es-tu-derecho/serpavi\n"
    "Place the Excel file in data/raw/ and use SERPAVIExtractor.extract_from_file()"
)


class SERPAVIExtractor(BaseExtractor):
    """Extract rental price reference data from SERPAVI (Ministerio de Vivienda).

    SERPAVI provides Excel downloads — automated download may require
    navigating their portal. Use extract_from_file() with a manually
    downloaded file, or extract() to attempt automated download.
    """

    name = "serpavi"

    def extract_from_file(self, excel_path: Path) -> Path:
        """Convert a manually downloaded SERPAVI Excel to normalized JSON."""
        import pandas as pd

        df = pd.read_excel(excel_path, engine="openpyxl")
        records = df.to_dict(orient="records")

        output = self.output_path("alquiler")
        output.write_text(json.dumps(records, ensure_ascii=False, indent=2, default=str))
        return output

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=30))
    async def _try_download(self, client: httpx.AsyncClient) -> bytes | None:
        resp = await client.get(f"{SERPAVI_BASE}/vivienda/alquila-bien-es-tu-derecho/serpavi")
        resp.raise_for_status()
        # TODO: parse HTML to find actual Excel download link
        return None

    async def extract(self, **kwargs) -> Path:
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            data = await self._try_download(client)

        if data is None:
            output = self.output_path("instructions")
            output.write_text(json.dumps({"manual_download": DOWNLOAD_HINT}, indent=2))
            return output

        raw_path = self.output_path("raw_excel")
        raw_path = raw_path.with_suffix(".xlsx")
        raw_path.write_bytes(data)
        return self.extract_from_file(raw_path)
