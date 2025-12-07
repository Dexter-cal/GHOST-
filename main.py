import os
from cryptography.fernet import Fernet
from ghost.orchestrator import GhostOrchestrator

def main():
    """
    The main entry point for the Ghost application.
    Initializes the orchestrator and runs a sample mission.
    """
    try:
        # Securely manage the vault key
        key = os.environ.get("GHOST_VAULT_KEY")
        if not key:
            print("GHOST_VAULT_KEY not found. Generating a new key for this session.")
            print("To persist the vault, set this environment variable: export GHOST_VAULT_KEY='your_key'")
            key = Fernet.generate_key().decode()
            os.environ["GHOST_VAULT_KEY"] = key
            print(f"New temporary key: {key}")

        # This mission will fail because the placeholder proxies and target
        # host are not real. This is for demonstration purposes.
        mission_params = {
            "persona_id": "mission_alpha",
            "target_host": "example.com",
        }

        orchestrator = GhostOrchestrator()
        orchestrator.create_and_run_mission(mission_params)

    except Exception as e:
        print(f"\nAn error occurred during the mission: {e}")
        print("This might be expected if placeholder values (like proxies or URLs) are not configured.")

if __name__ == "__main__":
    main()
