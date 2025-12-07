from enum import Enum

class PayloadFootprint(Enum):
    VAPOR = "Vapor (Tiny, single-purpose)"
    MIST = "Mist (Modular, quiet)"
    FOG = "Fog (Full capabilities, adaptive)"

class Payload:
    """
    Base class for all payloads managed by the GhostCasket.
    """
    def __init__(self, name, footprint: PayloadFootprint, content):
        self.name = name
        self.footprint = footprint
        self.content = content
        self.is_file_based = False

    def get_content(self):
        """
        Returns the payload's content.
        """
        return self.content

    def get_noise_prediction(self):
        """
        Provides a prediction of how 'noisy' this payload is likely to be.
        This is a simple heuristic based on footprint.
        """
        if self.footprint == PayloadFootprint.VAPOR:
            return "light drizzle (safe)"
        elif self.footprint == PayloadFootprint.MIST:
            return "gusty (caution)"
        elif self.footprint == PayloadFootprint.FOG:
            return "thunderstorm (noisy)"

class FilePayload(Payload):
    """
    A payload that is represented by a file on disk.
    """
    def __init__(self, name, footprint: PayloadFootprint, file_path):
        super().__init__(name, footprint, file_path)
        self.is_file_based = True
