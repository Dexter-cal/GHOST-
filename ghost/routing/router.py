import random
import time
import json
import os

class MirageRouter:
    """
    Manages multi-hop proxy chains, now with a fix for the runtime bug
    in get_exit_node to prevent crashes when no proxies are available.
    """
    def __init__(self, stealth_engine, config_path="config.json"):
        self.stealth_engine = stealth_engine
        self.config_path = config_path
        self.proxy_list = self._load_proxies_from_config()
        self.proxy_health = {proxy: {"successes": 0, "failures": 0} for proxy in self.proxy_list}

    def _load_proxies_from_config(self):
        """
        Loads a list of proxies from the config file with robust error handling.
        """
        if not os.path.exists(self.config_path):
            print(f"Warning: Config file not found at '{self.config_path}'. Using empty proxy list. Please create it from 'config.json.example'.")
            return []

        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)

            proxies = config.get("proxies", [])
            if not isinstance(proxies, list):
                print(f"Warning: 'proxies' key in '{self.config_path}' is not a list. Using empty proxy list.")
                return []

            return proxies

        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from '{self.config_path}'. The file may be malformed. Using empty proxy list.")
            return []
        except Exception as e:
            print(f"Warning: An unexpected error occurred while loading config: {e}. Using empty proxy list.")
            return []

    def _get_healthy_proxies(self, count=1):
        """
        Selects proxies based on their health.
        """
        if not self.proxy_list:
            return []
        sorted_proxies = sorted(self.proxy_list, key=lambda p: self._get_health_score(p), reverse=True)
        return sorted_proxies[:count]

    def _get_health_score(self, proxy):
        """
        Calculates a simple health score.
        """
        stats = self.proxy_health[proxy]
        if stats["failures"] == 0:
            return stats["successes"]
        return stats["successes"] / stats["failures"]

    def update_proxy_health(self, proxy, success=True):
        """
        Updates the health status of a proxy.
        """
        if proxy in self.proxy_health:
            if success:
                self.proxy_health[proxy]["successes"] += 1
            else:
                self.proxy_health[proxy]["failures"] += 1

    def get_proxy_chain(self, num_hops=3):
        """
        Returns a chain of healthy proxies, with smart retry logic.
        """
        if not self.proxy_list or len(self.proxy_list) < num_hops:
            print("Warning: Not enough proxies available to create a chain.")
            return []

        for attempt in range(3):
            chain = self._get_healthy_proxies(num_hops)
            if len(chain) == num_hops:
                return chain
            self.stealth_engine.wait()

        raise ConnectionError("Failed to create a healthy proxy chain.")

    def get_exit_node(self):
        """
        Returns a single healthy exit node, or None if no healthy proxies are available.
        """
        healthy_proxies = self._get_healthy_proxies(1)
        if not healthy_proxies:
            return None
        return healthy_proxies[0]
