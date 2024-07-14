from typing import Any, Dict, List

from normalize.base import Normalizer


class CrowdStrikeNormalizer(Normalizer):

    def normalize(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []
        for host in data:
            # print(host)
            # exit()
            normalized.append(
                {
                    "host_id": host["device_id"],
                    "platform": host["platform_name"],
                    "ip_addresses": [host["local_ip"], host["external_ip"]],
                    "mac_address": self.normalize_mac_address(host["mac_address"]),
                    "hostnames": [host["hostname"]],
                    "os": host["os_version"],
                    "last_seen": host["last_seen"],
                    "location": {"city": None, "state": None, "country": None},
                    "software": [],
                    "open_ports": [],
                }
            )
        return normalized
