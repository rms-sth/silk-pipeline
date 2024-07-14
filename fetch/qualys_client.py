from typing import Any, Dict, List

from fetch.base_client import BaseClient


class QualysClient(BaseClient):
    async def fetch_hosts(self) -> List[Dict[str, Any]]:
        return await self._get(
            "api/qualys/hosts/get",
            params={
                "skip": 5,
                "limit": 2,
            },
        )
