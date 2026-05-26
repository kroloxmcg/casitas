import base64
import json
from pathlib import Path

import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

from src.config import settings

from .base import BaseExtractor

TOKEN_URL = "https://api.idealista.com/oauth/token"
SEARCH_URL = "https://api.idealista.com/3.5/es/search"


class IdealistaExtractor(BaseExtractor):
    name = "idealista"

    def __init__(self):
        self._token: str | None = None

    async def _get_token(self, client: httpx.AsyncClient) -> str:
        if self._token:
            return self._token

        credentials = f"{settings.idealista_api_key}:{settings.idealista_api_secret}"
        encoded = base64.b64encode(credentials.encode()).decode()

        resp = await client.post(
            TOKEN_URL,
            headers={
                "Authorization": f"Basic {encoded}",
                "Content-Type": "application/x-www-form-urlencoded",
            },
            data={"grant_type": "client_credentials"},
        )
        resp.raise_for_status()
        self._token = resp.json()["access_token"]
        return self._token

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(min=2, max=30))
    async def _search(
        self,
        client: httpx.AsyncClient,
        token: str,
        *,
        center: str = "40.4168,-3.7038",
        distance: int = 15000,
        operation: str = "sale",
        property_type: str = "homes",
        page: int = 1,
    ) -> dict:
        resp = await client.post(
            SEARCH_URL,
            headers={"Authorization": f"Bearer {token}"},
            data={
                "center": center,
                "distance": distance,
                "operation": operation,
                "propertyType": property_type,
                "numPage": page,
                "maxItems": 50,
                "order": "publicationDate",
                "sort": "desc",
            },
        )
        resp.raise_for_status()
        return resp.json()

    async def extract(
        self,
        *,
        center: str = "40.4168,-3.7038",
        distance: int = 15000,
        operation: str = "sale",
        max_pages: int = 2,
    ) -> Path:
        all_listings = []
        async with httpx.AsyncClient(timeout=30) as client:
            token = await self._get_token(client)
            for page in range(1, max_pages + 1):
                result = await self._search(
                    client,
                    token,
                    center=center,
                    distance=distance,
                    operation=operation,
                    page=page,
                )
                elements = result.get("elementList", [])
                all_listings.extend(elements)
                if page >= result.get("totalPages", 1):
                    break

        output = self.output_path(operation)
        output.write_text(json.dumps(all_listings, ensure_ascii=False, indent=2))
        return output
