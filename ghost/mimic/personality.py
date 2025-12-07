class HostPersonality:
    """
    Learns and clones the 'temperament' of a target host, allowing Ghost
    to adapt its interaction patterns for maximum stealth.
    """
    def __init__(self, host_id):
        self.host_id = host_id
        self.behavior_map = {
            "response_times": [],
            "preferred_ciphers": {},
            "peak_traffic_hours": (0, 0), # (start_hour, end_hour)
            "aggressively_cached_endpoints": set(),
        }

    def learn_from_interaction(self, response_time, cipher=None, endpoint=None, is_cached=False):
        """
        Updates the host's personality map based on a single interaction.
        """
        self.behavior_map["response_times"].append(response_time)
        if len(self.behavior_map["response_times"]) > 200:
            self.behavior_map["response_times"].pop(0)

        if cipher:
            self.behavior_map["preferred_ciphers"][cipher] = self.behavior_map["preferred_ciphers"].get(cipher, 0) + 1

        if is_cached and endpoint:
            self.behavior_map["aggressively_cached_endpoints"].add(endpoint)

        # In a real system, peak traffic hours would be learned over a much longer period.

    def get_adaptive_delay_multiplier(self):
        """
        Returns a multiplier for delays based on the host's typical response time.
        If we are slower than the host's average, we might look suspicious.
        """
        if not self.behavior_map["response_times"]:
            return 1.0

        avg_response_time = sum(self.behavior_map["response_times"]) / len(self.behavior_map["response_times"])

        # This is a simple heuristic: if the host is fast, we should be too (within limits).
        if avg_response_time < 0.5:
            return 0.8 # Be a bit quicker
        elif avg_response_time > 2.0:
            return 1.5 # Be a bit slower, more cautious

        return 1.0

    def should_use_cache(self, endpoint):
        """
        Determines if an endpoint is likely to be aggressively cached.
        """
        return endpoint in self.behavior_map["aggressively_cached_endpoints"]

    def get_preferred_cipher(self):
        """
        Returns the most frequently observed TLS cipher.
        """
        if not self.behavior_map["preferred_ciphers"]:
            return None
        return max(self.behavior_map["preferred_ciphers"], key=self.behavior_map["preferred_ciphers"].get)
