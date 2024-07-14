from typing import Any, Dict, List

from normalize.base import Normalizer


class QualysNormalizer(Normalizer):

    def normalize(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        normalized = []
        for host in data:
            location_parts = host["agentInfo"]["location"].split(",")
            location = {
                "city": location_parts[0] if len(location_parts) > 0 else None,
                "state": location_parts[1] if len(location_parts) > 1 else None,
                "country": location_parts[2] if len(location_parts) > 2 else None,
            }
            mac_address = ""
            mac_addresses = {
                interface["HostAssetInterface"]["macAddress"]
                for interface in host["networkInterface"]["list"]
                if "macAddress" in interface["HostAssetInterface"]
            }
            if mac_addresses:
                mac_address = mac_addresses.pop()

            normalized_data = {
                "host_id": str(host["_id"]),
                "platform": host["agentInfo"]["platform"],
                "ip_addresses": [
                    interface["HostAssetInterface"]["address"]
                    for interface in host["networkInterface"]["list"]
                ],
                "mac_address": self.normalize_mac_address(mac_address),
                "hostnames": [
                    interface["HostAssetInterface"]["hostname"]
                    for interface in host["networkInterface"]["list"]
                ],
                "os": host["os"],
                "last_seen": host["agentInfo"]["lastCheckedIn"]["$date"],
                "location": location,
                "software": [
                    software["HostAssetSoftware"]["name"]
                    for software in host["software"]["list"]
                ],
                "open_ports": [
                    {
                        "port": port["HostAssetOpenPort"]["port"],
                        "protocol": port["HostAssetOpenPort"]["protocol"],
                    }
                    for port in host["openPort"]["list"]
                ],
            }
            # print(normalized_data)
            # exit()
            normalized.append(normalized_data)
        return normalized
