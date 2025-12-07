from .base import Payload, FilePayload, PayloadFootprint

class GhostCasket:
    """
    Manages the creation, storage, and wrapping of payloads, and includes
    the Noise Prediction Engine to estimate the subtlety of operations.
    """
    def __init__(self):
        self.payloads = {}

    def create_payload(self, name, footprint: PayloadFootprint, content, is_file=False):
        """
        Creates a new payload and stores it in the casket.
        """
        if is_file:
            payload = FilePayload(name, footprint, content)
        else:
            payload = Payload(name, footprint, content)

        self.payloads[name] = payload
        print(f"Payload '{name}' created with footprint '{footprint.value}'.")
        print(f"Noise Prediction: This payload has a '{payload.get_noise_prediction()}' noise level.")
        return payload

    def get_payload(self, name):
        """
        Retrieves a payload from the casket.
        """
        return self.payloads.get(name)

    def list_payloads(self):
        """
        Lists all available payloads and their noise predictions.
        """
        for name, payload in self.payloads.items():
            print(f"- {name} ({payload.footprint.value}): {payload.get_noise_prediction()}")
