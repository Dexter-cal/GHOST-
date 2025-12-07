import argparse
import os
from cryptography.fernet import Fernet
from ghost.orchestrator import GhostOrchestrator

def main():
    """
    The main entry point for the Ghost Command-Line Interface.
    """
    key = os.environ.get("GHOST_VAULT_KEY")
    if not key:
        print("GHOST_VAULT_KEY not found. Generating a new key for this session.")
        key = Fernet.generate_key().decode()
        os.environ["GHOST_VAULT_KEY"] = key
        print(f"New temporary key: {key}")

    parser = argparse.ArgumentParser(description="Ghost: A Stealthy Pentesting Companion")
    subparsers = parser.add_subparsers(dest="command", required=True, help="Available commands")

    # --- 'create' command ---
    create_parser = subparsers.add_parser("create", help="Create a new account on a target domain.")
    create_parser.add_argument("--domain", required=True, help="Target domain (must match a key in site_rules.json).")
    create_parser.add_argument("--engagement", required=True, help="Engagement ID to store credentials under.")
    create_parser.add_argument("--password-strategy", choices=["random", "memorable", "pattern"], default="random", help="Password generation strategy.")
    create_parser.add_argument("--persona", default="ghost_persona", help="A name for the persona to be created for this account.")

    # --- 'list' command ---
    list_parser = subparsers.add_parser("list", help="List credentials for an engagement.")
    list_parser.add_argument("--engagement", required=True, help="The engagement ID to list credentials for.")

    # --- 'login' command ---
    login_parser = subparsers.add_parser("login", help="Log in to a domain using stored credentials.")
    login_parser.add_argument("--domain", required=True, help="Target domain (must match a key in site_rules.json).")
    login_parser.add_argument("--username", required=True, help="The username to log in with.")
    login_parser.add_argument("--engagement", required=True, help="Engagement ID where credentials are stored.")

    # --- 'persona' command ---
    persona_parser = subparsers.add_parser("persona", help="Manage persistent personas.")
    persona_subparsers = persona_parser.add_subparsers(dest="persona_command", required=True)
    warmup_parser = persona_subparsers.add_parser("warmup", help="Run a warm-up mission for a persona.")
    warmup_parser.add_argument("--engagement", required=True, help="Engagement ID where the persona is stored.")
    warmup_parser.add_argument("--persona", required=True, help="The persona ID (username) to warm up.")
    warmup_parser.add_argument("--domain", required=True, help="The target domain for warm-up activities.")


    args = parser.parse_args()
    orchestrator = GhostOrchestrator()

    if args.command == "create":
        mission_params = {
            "target_domain": args.domain,
            "engagement_id": args.engagement,
            "password_strategy": args.password_strategy,
            "persona_id": args.persona,
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
    elif args.command == "persona" and args.persona_command == "warmup":
        mission_params = {
            "engagement_id": args.engagement,
            "persona_id": args.persona,
            "target_domain": args.domain,
        }
        orchestrator.run_persona_warmup_mission(mission_params)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\nAn error occurred: {e}")
