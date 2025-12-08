from bitcoinlib.wallets import Wallet, wallet_create_or_open
from bitcoinlib.mnemonic import Mnemonic

class WalletManager:
    """
    Manages the creation of secure, hierarchical deterministic (HD) wallets
    using the BIP39 standard.
    """
    def __init__(self):
        pass

    def create_new_wallet(self, wallet_name, passphrase=None):
        """
        Creates a new HD wallet.

        Args:
            wallet_name (str): A name for the new wallet.
            passphrase (str, optional): An optional passphrase for extra security.

        Returns:
            tuple: A tuple containing the wallet object and its mnemonic seed phrase.
        """
        print(f"WalletManager: Creating new wallet '{wallet_name}'...")

        # 1. Generate a new mnemonic (seed phrase)
        mnemonic = Mnemonic().generate()

        # 2. Create the wallet from the mnemonic
        # The bitcoinlib library handles the derivation of the master key.
        wallet = wallet_create_or_open(
            wallet_name,
            keys=mnemonic,
            passphrase=passphrase,
            network='bitcoin' # or 'testnet'
        )

        print(f"WalletManager: Wallet '{wallet_name}' created successfully.")
        print("IMPORTANT: Securely back up the following seed phrase. It is the only way to recover your wallet.")

        return wallet, mnemonic
