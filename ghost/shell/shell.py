import readline

class GhostShell:
    """
    An adaptive and resilient command relay with a 'Silent-Consent'
    mode to ensure operator control over noisy actions.
    """
    def __init__(self, stealth_engine):
        self.stealth_engine = stealth_engine
        self.history = []

    def _get_consent(self, action_description, noise_level):
        """
        Asks the operator for consent before performing a potentially
        noisy action.
        """
        if noise_level in ["gusty (caution)", "thunderstorm (noisy)"]:
            prompt = f"GhostShell: The action '{action_description}' has a noise level of '{noise_level}'. Proceed? (y/n): "
            answer = input(prompt).lower()
            return answer == 'y'
        return True # Automatically consent for safe actions

    def execute_command(self, command, noise_level="light drizzle (safe)"):
        """
        Executes a command, respecting the Silent-Consent mode.
        """
        self.history.append(command)

        if self._get_consent(command, noise_level):
            print(f"GhostShell: Executing '{command}'...")
            # In a real implementation, this would send the command to a
            # remote agent via a covert channel (e.g., GhostLink).
            self.stealth_engine.wait()
            print("GhostShell: Command executed. (Simulated)")
        else:
            print(f"GhostShell: Action '{command}' aborted by operator.")

    def show_history(self):
        """
        Displays the command history.
        """
        print("--- GhostShell History ---")
        for i, cmd in enumerate(self.history):
            print(f"{i+1}: {cmd}")
        print("--------------------------")
