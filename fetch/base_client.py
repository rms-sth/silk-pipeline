from abc import ABC, abstractmethod
from typing import Any, Dict, List

import httpx


class BaseClient(ABC):
    def __init__(self, api_url: str, token: str) -> None:
        self.api_url = api_url
        self.token = token

    @abstractmethod
    async def fetch_hosts(self) -> List[Dict[str, Any]]:
        pass

    async def _get(self, endpoint: str, params: dict = {}) -> Any:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.api_url}/{endpoint}",
                headers={"token": f"{self.token}"},
                params=params,
            )
            response.raise_for_status()
            return response.json()
