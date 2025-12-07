from enum import Enum
import time

class PersonaState(Enum):
    NEW = "new"
    WARMING_UP = "warming_up"
    ACTIVE = "active"
    COLLAPSED = "collapsed"

class LifecycleManager:
    """
    Manages the state and evolution of persistent personas.
    """
    def __init__(self, vault):
        self.vault = vault

    def update_persona_state(self, engagement_id, persona, new_state: PersonaState):
        """
        Updates the state of a persona and saves it back to the vault.
        """
        persona["state"] = new_state.value
        persona["last_state_change"] = time.time()
        self.vault.store_persona(engagement_id, persona)
        print(f"LifecycleManager: Persona '{persona['persona_id']}' state changed to '{new_state.value}'.")

    def get_persona_state(self, persona):
        """
        Retrieves the current state of a persona.
        """
        return persona.get("state", PersonaState.NEW.value)
