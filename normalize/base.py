import re
from abc import ABC, abstractmethod


class Normalizer(ABC):
    @abstractmethod
    def normalize(self, data):
        pass

    def normalize_mac_address(self, mac: str) -> str:
        # Normalize MAC address to a consistent format (e.g., all colons)
        return ":".join(re.findall("..", mac.replace("-", "").replace(":", "")))
