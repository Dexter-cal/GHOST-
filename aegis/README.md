# Aegis: A Secure Crypto Management System

Aegis is a command-line tool for the secure creation and management of cryptocurrency wallets. It is designed with a security-first philosophy, prioritizing the protection of sensitive key material through strong encryption and a secure workflow.

**This is a foundational implementation and is not yet ready for use with real funds.**

## Features

- **Secure Wallet Creation:** Generates new Hierarchical Deterministic (HD) wallets using the BIP39 standard.
- **Encrypted Keystore:** All sensitive wallet data is stored in a secure vault, encrypted with AES-256.
- **Strong Key Derivation:** Uses Argon2id to derive the encryption key from your password, providing protection against brute-force attacks.
- **Command-Line Interface:** A simple and intuitive CLI for managing your wallets.

## Installation

1.  **Install Dependencies:**
    Aegis is part of the Ghost project. Ensure you have installed all dependencies from the root `requirements.txt` file.
    ```bash
    pip install -r requirements.txt
    ```

## Usage

The main entry point for Aegis is the `aegis_cli.py` script. All operations require a vault password, which is used to encrypt and decrypt your wallet data.

### `wallet create`
Create a new, secure HD wallet. You will be prompted for a vault password.

```bash
python3 aegis_cli.py wallet create --name my_first_wallet
```

This will generate a new wallet and display its **seed phrase (mnemonic)**. **You must back up this seed phrase in a secure, offline location.** It is the only way to recover your wallet if you forget your vault password or lose your vault file.

For extra security, you can add a BIP39 passphrase to your wallet:
```bash
python3 aegis_cli.py wallet create --name my_secure_wallet --passphrase
```
You will be prompted for an additional passphrase.

### `wallet show`
Display basic information about a wallet stored in the vault. You will be prompted for the vault password that was used to create the wallet.

```bash
python3 aegis_cli.py wallet show --name my_first_wallet
```
