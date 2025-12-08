import json
from cryptography.fernet import Fernet

class MasterVault:
    """
    A comprehensive, secure vault for storing all data related to a Ghost
    identity, including personas, credentials, session data, and more.
    """
    def __init__(self, key):
        self.fernet = Fernet(key)
        self.engagements = {}

    def create_engagement(self, engagement_id):
        if engagement_id not in self.engagements:
            self.engagements[engagement_id] = {}
            print(f"MasterVault: New engagement segment '{engagement_id}' created.")

    def _store_item(self, engagement_id, item_key, value):
        if engagement_id not in self.engagements:
            raise ValueError("Engagement segment does not exist.")
        encrypted_value = self.fernet.encrypt(value.encode())
        self.engagements[engagement_id][item_key] = encrypted_value

    def _retrieve_item(self, engagement_id, item_key):
        if engagement_id not in self.engagements or item_key not in self.engagements[engagement_id]:
            return None
        encrypted_value = self.engagements[engagement_id][item_key]
        return self.fernet.decrypt(encrypted_value).decode()

    def store_account_data(self, engagement_id, username, data_type, data):
        """
        Stores a specific piece of data for an account (e.g., password, email, cookies).
        'data' will be serialized to JSON.
        """
        key = f"acct_{username}_{data_type}"
        value = json.dumps(data)
        self._store_item(engagement_id, key, value)
        print(f"MasterVault: Stored '{data_type}' for account '{username}'.")

    def retrieve_account_data(self, engagement_id, username, data_type):
        """
        Retrieves a specific piece of data for an account.
        """
        key = f"acct_{username}_{data_type}"
        value_json = self._retrieve_item(engagement_id, key)
        if value_json:
            return json.loads(value_json)
        return None

    def store_persona(self, engagement_id, persona):
        persona_id = persona["persona_id"]
        self._store_item(engagement_id, f"persona_{persona_id}", json.dumps(persona))
        print(f"MasterVault: Stored persona '{persona_id}'.")

    def retrieve_persona(self, engagement_id, persona_id):
        persona_json = self._retrieve_item(engagement_id, f"persona_{persona_id}")
        if persona_json:
            return json.loads(persona_json)
        return None

    def list_accounts_in_engagement(self, engagement_id):
        """
        Lists all accounts (usernames) stored within an engagement.
        """
        if engagement_id not in self.engagements:
            return []

        accounts = set()
        for key in self.engagements[engagement_id].keys():
            if key.startswith("acct_"):
                parts = key.split('_')
                if len(parts) > 1:
                    accounts.add(parts[1])
        return list(accounts)
