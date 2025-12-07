# Ghost: A Stealthy Pentesting Companion

Ghost is a modular and extensible framework for stealthy, authorized pentesting. It is designed to mimic human behavior, maintain a low profile, and provide a powerful suite of tools for reconnaissance, automation, and operational security.

## Features

- **Stealthy by Design:** Core philosophy is to blend in with normal traffic and user behavior.
- **Modular Architecture:** Easily extensible with new capabilities.
- **Human Mimicry:** Simulates human-like typing, mouse movements, and browsing patterns.
- **Secure Vault:** Encrypted storage for credentials and other sensitive data.
- **Command-Line Interface:** A powerful CLI for managing missions and accounts.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd ghost-project
    ```

2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Install a WebDriver:**
    Ghost uses Selenium for browser automation and requires a WebDriver. Please download and install the appropriate WebDriver for your browser (e.g., ChromeDriver) and ensure it is in your system's PATH.

## Configuration

1.  **Vault Key:**
    Ghost requires an encryption key for its secure vault. You can set this as an environment variable. If you don't, a temporary key will be generated for each session.

    ```bash
    export GHOST_VAULT_KEY='your_super_secret_key_here'
    ```

2.  **Proxies:**
    Create a `config.json` file from the `config.json.example` template and add your list of proxies.

3.  **Site Rules:**
    Create a `site_rules.json` file from the `site_rules.json.example` template. This file is crucial for the `create` and `login` commands. You must define the URLs and CSS selectors for the websites you want to automate.

## Usage (CLI)

The main entry point for Ghost is the `ghost_cli.py` script.

### `create`
Create a new account on a target website.

```bash
python3 ghost_cli.py create --domain example.com --engagement project_hydra
```

### `list`
List the credentials stored for a specific engagement.

```bash
python3 ghost_cli.py list --engagement project_hydra
```

### `login`
Log in to a website using stored credentials.

```bash
python3 ghost_cli.py login --domain example.com --username ghost_xxxx --engagement project_hydra
```
