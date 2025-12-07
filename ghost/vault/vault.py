import json
from cryptography.fernet import Fernet

class MemoryVault:
    """
    An enhanced, secure vault now capable of storing and retrieving
    entire persona objects for long-term persistence.
    """
    def __init__(self, key):
        self.fernet = Fernet(key)
        self.engagements = {} # {engagement_id: {storage_key: encrypted_value}}

    def create_engagement(self, engagement_id):
        """Creates a new, isolated data segment for an engagement."""
        if engagement_id not in self.engagements:
            self.engagements[engagement_id] = {}
            print(f"Vault: New engagement segment '{engagement_id}' created.")

    def _store_item(self, engagement_id, item_key, value):
        """A generic method to store an encrypted item."""
        if engagement_id not in self.engagements:
            raise ValueError("Engagement segment does not exist.")
        encrypted_value = self.fernet.encrypt(value.encode())
        self.engagements[engagement_id][item_key] = encrypted_value

    def _retrieve_item(self, engagement_id, item_key):
        """A generic method to retrieve a decrypted item."""
        if engagement_id not in self.engagements or item_key not in self.engagements[engagement_id]:
            return None
        encrypted_value = self.engagements[engagement_id][item_key]
        return self.fernet.decrypt(encrypted_value).decode()

    def store_credential(self, engagement_id, credential_name, value):
        """Stores a simple credential string."""
        self._store_item(engagement_id, f"cred_{credential_name}", value)
        print(f"Vault: Stored credential '{credential_name}' in '{engagement_id}'.")

    def retrieve_credential(self, engagement_id, credential_name):
        """Retrieves a simple credential string."""
        return self._retrieve_item(engagement_id, f"cred_{credential_name}")

    def store_persona(self, engagement_id, persona):
        """Serializes and stores a persona object."""
        persona_id = persona["persona_id"]
        persona_json = json.dumps(persona)
        self._store_item(engagement_id, f"persona_{persona_id}", persona_json)
        print(f"Vault: Stored persona '{persona_id}' in '{engagement_id}'.")

    def retrieve_persona(self, engagement_id, persona_id):
        """Retrieves and deserializes a persona object."""
        persona_json = self._retrieve_item(engagement_id, f"persona_{persona_id}")
        if persona_json:
            return json.loads(persona_json)
        return None

    def retrieve_engagement_credentials(self, engagement_id):
        """Retrieves all simple credentials for an engagement."""
        if engagement_id not in self.engagements:
            return None
        credentials = {}
        for key, enc_value in self.engagements[engagement_id].items():
            if key.startswith("cred_"):
                try:
                    cred_name = key.replace("cred_", "", 1)
                    credentials[cred_name] = self.fernet.decrypt(enc_value).decode()
                except Exception:
                    credentials[cred_name] = "[DECRYPTION_ERROR]"
        return credentials
