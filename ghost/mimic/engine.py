import time
import random
import os
from .personality import HostPersonality

class StealthEngine:
    """
    The central nervous system for Ghost's stealth operations, now with
    environmental awareness, host-specific personality cloning, and more organic timing.
    """
    def __init__(self):
        self.telemetry = {
            "latency_history": [],
            "error_rate": 0.0,
            "response_hashes": {},
            "tls_fingerprints": {},
        }
        self.mode = 'normal'
        self.alerts = []
        self.host_personalities = {} # Maps host_id to HostPersonality object

    def _get_host_personality(self, host_id):
        """
        Retrieves or creates a personality profile for a given host.
        """
        if host_id not in self.host_personalities:
            self.host_personalities[host_id] = HostPersonality(host_id)
        return self.host_personalities[host_id]

    def update_telemetry(self, host_id, latency, success=True, response_content=b"", tls_fingerprint=None, endpoint=None, is_cached=False):
        """
        Updates telemetry and learns from the interaction for a specific host.
        """
        # General telemetry updates
        self.telemetry["latency_history"].append(latency)
        # ... (rest of the telemetry logic as before) ...

        # Update host-specific personality
        host_personality = self._get_host_personality(host_id)
        host_personality.learn_from_interaction(latency, cipher=tls_fingerprint, endpoint=endpoint, is_cached=is_cached)

        self._analyze_for_blindspots()
        self._check_for_reflexive_backoff()

    def _analyze_for_blindspots(self):
        """
        Analyzes telemetry for signs of honeypots or monitored environments.
        This is a simplified heuristic.
        """
        # Check for too many identical responses (potential uniform error pages)
        if len(self.telemetry["response_hashes"]) > 10:
            most_common = max(self.telemetry["response_hashes"].values())
            if most_common / sum(self.telemetry["response_hashes"].values()) > 0.8:
                self.alerts.append("Sensory Blindspot: High frequency of identical responses. Possible honeypot or WAF.")

        # Check for a single, recurring TLS fingerprint (potential proxy/interception)
        if len(self.telemetry["tls_fingerprints"]) == 1 and sum(self.telemetry["tls_fingerprints"].values()) > 10:
            self.alerts.append("Sensory Blindspot: All connections share the same TLS fingerprint. Possible interception.")


    def _check_for_reflexive_backoff(self):
        """
        Analyzes metrics to decide if a back-off is needed.
        """
        avg_latency = sum(self.telemetry["latency_history"]) / len(self.telemetry["latency_history"]) if self.telemetry["latency_history"] else 0

        if self.telemetry["error_rate"] > 0.5 or (len(self.telemetry["latency_history"]) > 10 and avg_latency > 2.0):
            self.mode = 'cautious'
        elif self.telemetry["error_rate"] > 0.8 or (len(self.telemetry["latency_history"]) > 10 and avg_latency > 5.0):
            self.mode = 'silent'
        elif self.telemetry["error_rate"] < 0.1 and avg_latency < 1.0:
            self.mode = 'normal'

    def get_quantum_random_delay(self, host_id=None):
        """
        Calculates a delay using organic randomness, adapted for the specific host.
        """
        # Base delay from general stealth mode
        if self.mode == 'silent':
            base_delay = random.uniform(5, 15)
        elif self.mode == 'cautious':
            base_delay = random.uniform(1, 5)
        else: # 'normal'
            base_delay = random.uniform(0.1, 1.0)

        # Adapt delay based on host personality
        if host_id:
            host_personality = self._get_host_personality(host_id)
            base_delay *= host_personality.get_adaptive_delay_multiplier()

        # Mix in OS-level entropy
        os_entropy = int.from_bytes(os.urandom(2), 'big') / 65535.0
        jitter = 0.5 + os_entropy

        return base_delay * jitter

    def wait(self, host_id=None):
        """
        Pauses execution for a quantum-random, host-adapted duration.
        """
        delay = self.get_quantum_random_delay(host_id)
        time.sleep(delay)

    def get_alerts(self):
        """
        Returns a list of detected alerts.
        """
        return self.alerts
