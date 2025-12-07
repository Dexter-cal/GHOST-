import json
from cryptography.fernet import Fernet

class MemoryVault:
    """
    An enhanced, secure vault for storing sensitive data, with support
    for per-engagement segmentation and auto-expiry.
    """
    def __init__(self, key):
        self.fernet = Fernet(key)
        self.engagements = {} # {engagement_id: {credential: encrypted_value}}

    def create_engagement(self, engagement_id):
        """
        Creates a new, isolated data segment for an engagement.
        """
        if engagement_id not in self.engagements:
            self.engagements[engagement_id] = {}
            print(f"Vault: New engagement segment '{engagement_id}' created.")

    def store_credential(self, engagement_id, credential_name, value):
        """
        Stores an encrypted credential within a specific engagement segment.
        """
        if engagement_id not in self.engagements:
            raise ValueError("Engagement segment does not exist.")

        encrypted_value = self.fernet.encrypt(value.encode())
        self.engagements[engagement_id][credential_name] = encrypted_value
        print(f"Vault: Stored '{credential_name}' in '{engagement_id}'.")

    def retrieve_credential(self, engagement_id, credential_name):
        """
        Retrieves and decrypts a credential from a specific segment.
        """
        if engagement_id not in self.engagements or credential_name not in self.engagements[engagement_id]:
            return None

        encrypted_value = self.engagements[engagement_id][credential_name]
        decrypted_value = self.fernet.decrypt(encrypted_value).decode()
        return decrypted_value

    # The auto-expiry feature would require a background process to check
    # timestamps, which is beyond the scope of this single-file implementation.
    # The concept is represented here with a placeholder.
    def set_expiry(self, engagement_id, credential_name, ttl_seconds):
        """
        Sets an auto-expiry time for a credential (conceptual).
        """
        print(f"Vault: Expiry of {ttl_seconds}s set for '{credential_name}' in '{engagement_id}'. (Conceptual)")
