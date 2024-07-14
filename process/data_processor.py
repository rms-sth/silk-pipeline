from typing import Dict

from fetch.base_client import BaseClient
from normalize.base import Normalizer
from process.de_duplicator import DeDuplicator


class DataProcessor:
    def __init__(
        self,
        clients: Dict[str, BaseClient],
        normalizers: Dict[str, Normalizer],
        de_duplicator: DeDuplicator,
    ):
        self.clients = clients
        self.normalizers = normalizers
        self.de_duplicator = de_duplicator

    async def fetch_and_normalize_hosts(self):
        normalized_data = {}

        # Fetch and normalize data for each client
        for client_name, client in self.clients.items():
            data = await client.fetch_hosts()
            normalizer = self.normalizers.get(client_name)
            if normalizer:
                normalized_data[client_name] = normalizer.normalize(data)

        # Deduplicate merged data from all clients
        deduplicated_data = self.de_duplicator.de_duplicate_and_merge(
            *normalized_data.values()
        )

        return deduplicated_data
