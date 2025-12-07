import argparse
import os
from cryptography.fernet import Fernet
from ghost.orchestrator import GhostOrchestrator

def main():
    """
    The main entry point for the Ghost Command-Line Interface.
    """
    # --- Securely manage the vault key ---
    key = os.environ.get("GHOST_VAULT_KEY")
    if not key:
        print("GHOST_VAULT_KEY not found. Generating a new key for this session.")
        print("To persist the vault, set this environment variable: export GHOST_VAULT_KEY='your_key'")
        key = Fernet.generate_key().decode()
        os.environ["GHOST_VAULT_KEY"] = key
        print(f"New temporary key: {key}")

    # --- Setup the CLI Parser ---
    parser = argparse.ArgumentParser(description="Ghost: A Stealthy Pentesting Companion")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # --- 'create' command ---
    create_parser = subparsers.add_parser("create", help="Create a new account on a target domain.")
    create_parser.add_argument("--domain", required=True, help="The target domain (must match a key in site_rules.json).")
    create_parser.add_argument("--engagement", required=True, help="The engagement ID to store credentials under.")

    # --- 'list' command ---
    list_parser = subparsers.add_parser("list", help="List credentials stored in the vault for an engagement.")
    list_parser.add_argument("--engagement", required=True, help="The engagement ID to list credentials for.")

    # --- 'login' command ---
    login_parser = subparsers.add_parser("login", help="Log in to a target domain using stored credentials.")
    login_parser.add_argument("--domain", required=True, help="The target domain (must match a key in site_rules.json).")
    login_parser.add_argument("--username", required=True, help="The username of the account to log in with.")
    login_parser.add_argument("--engagement", required=True, help="The engagement ID where the credentials are stored.")

    args = parser.parse_args()

    # --- Command Dispatch ---
    orchestrator = GhostOrchestrator()

    if args.command == "create":
        mission_params = {
            "target_domain": args.domain,
            "engagement_id": args.engagement,
        }
        orchestrator.run_account_creation_mission(mission_params)
    elif args.command == "list":
        creds = orchestrator.vault.retrieve_engagement_credentials(args.engagement)
        if not creds:
            print(f"No credentials found for engagement '{args.engagement}'.")
        else:
            print(f"--- Credentials for Engagement: {args.engagement} ---")
            for name, value in creds.items():
                print(f"  {name}: {value}")
            print("------------------------------------------")
    elif args.command == "login":
        mission_params = {
            "target_domain": args.domain,
            "username": args.username,
            "engagement_id": args.engagement,
        }
        orchestrator.run_login_mission(mission_params)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nAn error occurred: {e}")
