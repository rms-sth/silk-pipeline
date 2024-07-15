from datetime import datetime, timedelta
from typing import Any, Dict, List

import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self, hosts: List[Dict[str, Any]]) -> None:
        self.hosts = hosts

    def _get_os_distribution(self) -> Dict[str, int]:
        os_counts = {}
        for host in self.hosts:
            # Assuming 'os' is a dictionary and has a 'name' field
            os = host["os"]["name"] if isinstance(host["os"], dict) else host["os"]
            if os in os_counts:
                os_counts[os] += 1
            else:
                os_counts[os] = 1
        return os_counts

    def _get_old_new_hosts(self) -> Dict[str, int]:
        old_threshold = datetime.now() - timedelta(days=30)
        old_hosts_count = sum(
            1
            for host in self.hosts
            if datetime.fromisoformat(host["last_seen"][:-1]) < old_threshold
        )
        new_hosts_count = len(self.hosts) - old_hosts_count
        return {"Old Hosts": old_hosts_count, "New Hosts": new_hosts_count}

    def plot_os_distribution(self) -> None:
        os_counts = self._get_os_distribution()
        plt.figure(figsize=(10, 6))
        plt.bar([key[:30] for key in os_counts], os_counts.values())
        plt.xlabel("Operating System")
        plt.ylabel("Number of Hosts")
        plt.title("Distribution of Hosts by Operating System")
        plt.savefig("hosts_by_os.png")
        plt.show()

    def plot_old_vs_new_hosts(self) -> None:
        host_counts = self._get_old_new_hosts()
        plt.figure(figsize=(10, 6))
        plt.bar(host_counts.keys(), host_counts.values())
        plt.xlabel("Host Category")
        plt.ylabel("Number of Hosts")
        plt.title("Old Hosts vs Newly Discovered Hosts")
        plt.savefig("old_vs_new_hosts.png")
        plt.show()
