from typing import Any, Dict, List


class DeDuplicator:

    def de_duplicate_and_merge(
        self, data1: List[Dict[str, Any]], data2: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        combined_data = data1 + data2
        deduplicated_data = {}

        for host in combined_data:
            mac_address = tuple(host["mac_address"])
            ip_addresses = tuple(host["ip_addresses"])
            key = (mac_address, ip_addresses)
            if key in deduplicated_data:
                deduplicated_data[key] = self.merge_hosts(deduplicated_data[key], host)
            else:
                deduplicated_data[key] = host

        return list(deduplicated_data.values())

    def merge_hosts(
        self, host1: Dict[str, Any], host2: Dict[str, Any]
    ) -> Dict[str, Any]:
        merged_host = host1.copy()

        merged_host["ip_addresses"] = list(
            set(host1["ip_addresses"] + host2["ip_addresses"])
        )

        mac_address = ""
        mac_addresses = set(host1["mac_address"] + host2["mac_address"])
        if mac_addresses:
            mac_address = mac_addresses.pop()

        merged_host["mac_address"] = mac_address
        merged_host["hostnames"] = list(set(host1["hostnames"] + host2["hostnames"]))
        merged_host["software"] = list(set(host1["software"] + host2["software"]))
        merged_host["open_ports"] = list(
            {
                tuple(port.items()): port
                for port in (host1["open_ports"] + host2["open_ports"])
            }.values()
        )

        # Prefer non-null values for the last_seen, platform, os, and location fields
        merged_host["last_seen"] = max(host1["last_seen"], host2["last_seen"])
        merged_host["platform"] = (
            host1["platform"] if host1["platform"] else host2["platform"]
        )
        merged_host["os"] = host1["os"] if host1["os"] else host2["os"]
        merged_host["location"] = (
            host1["location"] if host1["location"] else host2["location"]
        )

        return merged_host
