import random
import time

class PersonalityGenerator:
    """
    Creates and manages evolving, stealth-integrated personas for Ghost,
    now with realistic name and username generation.
    """
    def __init__(self):
        self.personas = {}
        # In a real system, these would be loaded from larger data files.
        self.first_names = ["john", "jane", "alex", "emily", "chris", "katie"]
        self.last_names = ["smith", "jones", "williams", "brown", "davis", "miller"]

    def _generate_realistic_name(self):
        """Generates a random first and last name."""
        return random.choice(self.first_names), random.choice(self.last_names)

    def _generate_usernames(self, first, last):
        """Generates a list of potential usernames from a name."""
        year = random.randint(80, 99)
        return [
            f"{first[0]}{last}".lower(),
            f"{first}.{last}".lower(),
            f"{first}{last}{year}",
            f"{last}_{first}".lower(),
        ]

    def create_persona(self, persona_id, target_context=None):
        """
        Generates a new persona with a full, realistic identity.
        """
        first_name, last_name = self._generate_realistic_name()

        persona = {
            "persona_id": persona_id,
            "state": "new",
            "last_state_change": time.time(),
            "identity": {
                "first_name": first_name,
                "last_name": last_name,
                "potential_usernames": self._generate_usernames(first_name, last_name),
            },
            "header_profile": self._get_blended_header_profile(),
            "fingerprint_profile": self._get_minimal_fingerprint(),
            "typing_rhythm": self._get_typing_rhythm(),
            "sleep_schedule": self._get_sleep_schedule(),
        }
        self.personas[persona_id] = persona
        return persona

    # ... (rest of the methods for profile, fingerprint, etc. remain the same) ...
    def _get_blended_header_profile(self, target_context=None):
        common_profiles = [
            {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "Accept-Language": "en-US,en;q=0.9"},
            {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36", "Accept-Language": "en-GB,en;q=0.5"},
        ]
        return random.choice(common_profiles)

    def _get_minimal_fingerprint(self):
        return {
            "canvas_spoofing": True,
            "webgl_vendor": "Google Inc. (Intel)",
            "screen_resolution": random.choice(["1920x1080", "1366x768"]),
        }

    def _get_typing_rhythm(self):
        return {"wpm": random.randint(40, 80), "mistake_rate": random.uniform(0.01, 0.05)}

    def _get_sleep_schedule(self):
        sleep_start = random.randint(21, 23)
        sleep_end = random.randint(5, 8)
        return (sleep_start, sleep_end)
