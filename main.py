import os
from cryptography.fernet import Fernet
from ghost.orchestrator import GhostOrchestrator

def main():
    """
    The main entry point for the Ghost application.
    Demonstrates both a recon mission and an account creation mission.
    """
    try:
        # --- Securely manage the vault key ---
        key = os.environ.get("GHOST_VAULT_KEY")
        if not key:
            print("GHOST_VAULT_KEY not found. Generating a new key for this session.")
            print("To persist the vault, set this environment variable: export GHOST_VAULT_KEY='your_key'")
            key = Fernet.generate_key().decode()
            os.environ["GHOST_VAULT_KEY"] = key
            print(f"New temporary key: {key}")

        orchestrator = GhostOrchestrator()

        # --- Mission 1: Reconnaissance (Example) ---
        # This mission will likely fail if placeholder values aren't configured,
        # which is expected for this demonstration.
        print("\n### DEMONSTRATING RECON MISSION ###")
        recon_mission_params = {
            "persona_id": "recon_alpha",
            "target_host": "example.com",
        }
        orchestrator.create_and_run_mission(recon_mission_params)

        # --- Mission 2: Account Creation (Example) ---
        # This mission requires a 'site_rules.json' file to be created.
        # It will fail gracefully if the file does not exist.
        print("\n### DEMONSTRATING ACCOUNT CREATION MISSION ###")
        account_creation_params = {
            "persona_id": "acct_creator_beta",
            "target_domain": "example.com", # Must match a key in your site_rules.json
            "engagement_id": "project_hydra",
        }
        orchestrator.run_account_creation_mission(account_creation_params)

    except Exception as e:
        print(f"\nAn error occurred during the mission: {e}")
        print("This might be expected if placeholder values (like proxies or site rules) are not configured.")

if __name__ == "__main__":
    main()
