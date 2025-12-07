import random
import time

class PersonalityGenerator:
    """
    Creates and manages evolving, stealth-integrated personas for Ghost,
    now with support for a 'collapsed' (dormant) state.
    """
    def __init__(self):
        self.personas = {}

    def create_persona(self, persona_id, target_context=None):
        """
        Generates a new persona with a set of realistic, blended characteristics.
        """
        persona = {
            "persona_id": persona_id,
            "status": "active",  # Can be 'active' or 'collapsed'
            "last_active_timestamp": time.time(),
            "header_profile": self._get_blended_header_profile(target_context),
            "fingerprint_profile": self._get_minimal_fingerprint(),
            "typing_rhythm": self._get_typing_rhythm(),
            "sleep_schedule": self._get_sleep_schedule(),
            "device_preferences": self._get_device_preferences(),
            "timezone": self._get_random_timezone(),
        }
        self.personas[persona_id] = persona
        return persona

    def collapse_persona(self, persona_id):
        """
        Sets a persona to a dormant, inactive state.
        """
        if persona_id in self.personas:
            self.personas[persona_id]["status"] = "collapsed"
            print(f"Persona {persona_id} collapsed.")

    def activate_persona(self, persona_id):
        """
        Activates a dormant persona.
        """
        if persona_id in self.personas:
            self.personas[persona_id]["status"] = "active"
            self.personas[persona_id]["last_active_timestamp"] = time.time()
            print(f"Persona {persona_id} activated.")

    def is_persona_sleeping(self, persona_id):
        """
        Checks if a persona is within its natural sleep schedule.
        """
        if persona_id not in self.personas:
            return False

        persona = self.personas[persona_id]
        if persona['status'] == 'collapsed':
            return True # A collapsed persona is always "sleeping"

        sleep_start, sleep_end = persona['sleep_schedule']
        current_hour_utc = int(time.strftime("%H", time.gmtime()))

        if sleep_start > sleep_end: # Overnight schedule
            return current_hour_utc >= sleep_start or current_hour_utc < sleep_end
        else:
            return sleep_start <= current_hour_utc < sleep_end

    # ... (rest of the methods from before) ...
    def _get_blended_header_profile(self, target_context=None):
        """
        Returns a dictionary of blended HTTP headers.
        In a real implementation, this would be far more sophisticated,
        learning from the target's typical traffic.
        """
        common_profiles = [
            {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Accept-Language": "en-US,en;q=0.9",
                "Accept-Encoding": "gzip, deflate, br",
            },
            {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                "Accept-Language": "en-GB,en;q=0.5",
                "Accept-Encoding": "gzip, deflate, br",
            }
        ]
        return random.choice(common_profiles)

    def _get_minimal_fingerprint(self):
        """
        Returns a profile for a common, minimal browser fingerprint.
        This aims to avoid unique characteristics that make a browser stand out.
        """
        return {
            "canvas_spoofing": True,
            "webgl_vendor": "Google Inc. (Intel)",
            "timezone": "UTC",
            "screen_resolution": random.choice(["1920x1080", "1366x768", "1536x864"]),
            "font_list": "default", # Use a common, default font list
            "protocol_shape": "standard_chrome", # Mimic standard Chrome TLS/HTTP2 behavior
        }

    def _get_typing_rhythm(self):
        """
        Returns a dictionary representing a typing rhythm.
        """
        return {
            "wpm": random.randint(40, 80),
            "mistake_rate": random.uniform(0.01, 0.05),
            "pause_frequency": random.uniform(0.1, 0.5),
            "pause_duration": random.uniform(0.1, 0.5),
        }

    def _get_sleep_schedule(self):
        """
        Returns a tuple representing a sleep schedule (in UTC hours).
        """
        sleep_start = random.randint(21, 23)
        sleep_end = random.randint(5, 8)
        return (sleep_start, sleep_end)

    def _get_device_preferences(self):
        """
        Returns a dictionary of device preferences.
        """
        return {
            "desktop_usage": random.uniform(0.4, 0.8),
            "mobile_usage": random.uniform(0.2, 0.6),
        }

    def _get_random_timezone(self):
        """
        Returns a random timezone.
        """
        timezones = ["UTC-8", "UTC-5", "UTC+1", "UTC+8"]
        return random.choice(timezones)
