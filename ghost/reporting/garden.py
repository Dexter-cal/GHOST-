import time

class MemoryGarden:
    """
    A living, navigable map of the engagement, providing intuitive
    visualizations and real-time stealth advice.
    """
    def __init__(self, stealth_engine):
        self.stealth_engine = stealth_engine
        self.events = [] # A list of dictionaries representing events

    def log_event(self, event_type, description, noise_level):
        """
        Logs a new event in the memory garden.
        """
        event = {
            "timestamp": time.time(),
            "type": event_type, # e.g., 'scan', 'delivery', 'alert'
            "description": description,
            "noise_level": noise_level, # From the Noise Prediction Engine
        }
        self.events.append(event)
        self._ghost_lantern_advice(event)

    def _ghost_lantern_advice(self, event):
        """
        Provides real-time stealth advice based on the latest event.
        """
        if event["noise_level"] == "thunderstorm (noisy)":
            print(f"Ghost Lantern: The last action, '{event['description']}', was very noisy. Consider switching to a quieter approach or waiting for a low-traffic window.")

        if event["type"] == "alert":
            print(f"Ghost Lantern: An alert was triggered: '{event['description']}'. This is a strong signal to back off and reassess. Silence is a virtue.")

    def render_garden(self):
        """
        Renders a simple, text-based representation of the memory garden.
        A real implementation would use a graphical library.
        """
        print("\n--- Ghost's Memory Garden ---")
        for event in self.events:
            timestamp_str = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(event["timestamp"]))

            # Simple visualization: vines for connections, flowers for alerts
            if event["type"] == "alert":
                icon = "🌸"
            elif event["type"] == "scan":
                icon = "🌿"
            else:
                icon = "🌱"

            print(f"{icon} [{timestamp_str}] {event['type'].upper()}: {event['description']} (Noise: {event['noise_level']})")
        print("---------------------------\n")
