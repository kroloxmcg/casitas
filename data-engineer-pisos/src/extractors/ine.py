import json
from pathlib import Path

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from .base import BaseExtractor

BASE_URL = "https://servicios.ine.es/wstempus/js/ES"


class INEExtractor(BaseExtractor):
    """Extract housing price index (IPV) data from INE API."""

    name = "ine"

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=30))
    async def _fetch_series(self, client: httpx.AsyncClient, series_id: str) -> list[dict]:
        resp = await client.get(f"{BASE_URL}/DATOS_SERIE/{series_id}", params={"nult": 40})
        resp.raise_for_status()
        return resp.json()

    async def extract(self, **kwargs) -> Path:
        series = {
            "ipv_general": "IPV914",
            "ipv_nueva": "IPV915",
            "ipv_segunda_mano": "IPV916",
        }

        results = {}
        async with httpx.AsyncClient(timeout=30) as client:
            for key, series_id in series.items():
                data = await self._fetch_series(client, series_id)
                results[key] = [
                    {
                        "periodo": entry.get("Nombre", entry.get("T3_Periodo", "")),
                        "valor": entry.get("Valor"),
                    }
                    for entry in data
                    if isinstance(entry, dict)
                ]

        output = self.output_path("ipv")
        output.write_text(json.dumps(results, ensure_ascii=False, indent=2))
        return output
