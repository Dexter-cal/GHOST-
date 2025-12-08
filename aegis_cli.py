import argparse
import getpass
from bitcoinlib.wallets import Wallet, wallet_delete
from bitcoinlib.mnemonic import Mnemonic

def main():
    """
    The main entry point for the Aegis CLI, now using bitcoinlib's
    native secure wallet management.
    """
    parser = argparse.ArgumentParser(description="Aegis: A Secure Crypto Management System")
    # ... (parser setup remains the same)
    wallet_parser = parser.add_subparsers(dest="command", required=True).add_parser("wallet")
    wallet_subparsers = wallet_parser.add_subparsers(dest="wallet_command", required=True)

    create_parser = wallet_subparsers.add_parser("create", help="Create a new wallet.")
    create_parser.add_argument("--name", required=True)
    create_parser.add_argument("--passphrase", action="store_true")

    show_parser = wallet_subparsers.add_parser("show", help="Show wallet public addresses.")
    show_parser.add_argument("--name", required=True)

    delete_parser = wallet_subparsers.add_parser("delete", help="Delete a wallet.")
    delete_parser.add_argument("--name", required=True)

    args = parser.parse_args()

    password = getpass.getpass("Enter wallet password (for encryption): ")

    if args.wallet_command == "create":
        mnemonic = Mnemonic().generate()
        print("\nIMPORTANT: Securely back up this seed phrase:")
        print(mnemonic)
        passphrase = getpass.getpass("Enter BIP39 passphrase (optional): ") if args.passphrase else None

        # bitcoinlib handles the encryption with the password
        Wallet.create(args.name, keys=mnemonic, passphrase=passphrase, password=password)
        print(f"\nWallet '{args.name}' created and securely stored.")

    elif args.wallet_command == "show":
        try:
            w = Wallet(args.name, password=password)
            print(f"\n--- Wallet: {w.name} ---")
            print(f"Network: {w.network.name}")
            print("\nFirst 5 Public Receiving Addresses:")
            for i in range(5):
                print(f"  {i}: {w.get_key(i).address}")
        except Exception as e:
            print(f"Error loading wallet. Is the password correct? Details: {e}")

    elif args.wallet_command == "delete":
        if input(f"Are you sure you want to PERMANENTLY delete wallet '{args.name}'? (y/n): ").lower() == 'y':
            wallet_delete(args.name)
            print(f"Wallet '{args.name}' deleted.")

if __name__ == "__main__":
    main()
