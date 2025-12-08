import argparse
import os
from cryptography.fernet import Fernet
from ghost.orchestrator import GhostOrchestrator

def main():
    """
    The main entry point for the Ghost CLI, with all commands fully wired up.
    """
    key = os.environ.get("GHOST_VAULT_KEY")
    # ... (key management)

    parser = argparse.ArgumentParser(description="Ghost: A Stealthy Pentesting Companion")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- 'account' command group ---
    acct_parser = subparsers.add_parser("account", help="Manage Ghost accounts.")
    acct_subparsers = acct_parser.add_subparsers(dest="account_command", required=True)

    # 'account create'
    create_parser = acct_subparsers.add_parser("create", help="Create one or more accounts.")
    create_parser.add_argument("--domain", required=True)
    create_parser.add_argument("--engagement", required=True)
    create_parser.add_argument("--count", type=int, default=1)

    # 'account list'
    list_parser = acct_subparsers.add_parser("list", help="List accounts for an engagement.")
    list_parser.add_argument("--engagement", required=True)

    # 'account login'
    login_parser = acct_subparsers.add_parser("login", help="Log in to capture a session.")
    login_parser.add_argument("--domain", required=True)
    login_parser.add_argument("--username", required=True)
    login_parser.add_argument("--engagement", required=True)

    # 'account launch'
    launch_parser = acct_subparsers.add_parser("launch", help="Launch a direct session for an account.")
    launch_parser.add_argument("--username", required=True)
    launch_parser.add_argument("--engagement", required=True)
    launch_parser.add_argument("--domain", required=True)

    args = parser.parse_args()
    orchestrator = GhostOrchestrator()

    if args.command == "account":
        if args.account_command == "create":
            orchestrator.run_account_creation_mission(vars(args))
        elif args.account_command == "list":
            # This is now fully functional
            accounts = orchestrator.vault.list_accounts_in_engagement(args.engagement)
            if not accounts:
                print(f"No accounts found for engagement '{args.engagement}'.")
            else:
                print(f"--- Accounts for Engagement: {args.engagement} ---")
                for username in accounts:
                    print(f"\n  Username: {username}")
                    # You would add more details here
                print("\n------------------------------------------")
        elif args.account_command == "login":
            orchestrator.run_login_mission(vars(args))
        elif args.account_command == "launch":
            orchestrator.run_session_teleporter_mission(vars(args))

if __name__ == "__main__":
    main()
