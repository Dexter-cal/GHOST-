# Ghost: A Stealthy Pentesting Companion

Ghost is a modular and extensible framework for stealthy, authorized pentesting. It is designed to mimic human behavior and provide a powerful suite of tools for reconnaissance, automation, and operational security.

## Features

- **Stealthy by Design:** Blends in with normal traffic and user behavior.
- **Human Mimicry:** Simulates human-like typing, browsing, and interaction.
- **Secure Vault:** Encrypted storage for all engagement data.
- **Powerful CLI:** A comprehensive command-line interface for all operations.
- **Lure Foundry:** A versatile engine for creating a wide variety of payload delivery vehicles.
- **Browser Auditing:** A safe, "BeEF-lite" capability for analyzing browser environments.
- **Batch Automation:** Create and manage entire stables of personas at once.

## Installation & Configuration

(Instructions remain the same. Ensure you run `pip install -r requirements.txt` to get the new dependencies.)

## Usage (CLI)

The main entry point for Ghost is the `ghost_cli.py` script.

### `create` (Batch Account Creation)
Create one or more accounts on a target website.

```bash
# Create a single account
python3 ghost_cli.py create --domain example.com --engagement project_hydra

# Create 5 accounts at once
python3 ghost_cli.py create --domain example.com --engagement project_hydra --count 5
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

### `audit` (Browser Auditing)
Run a safe, "BeEF-lite" style browser audit on a target URL. This will launch a browser, navigate to the URL, and inject a safe `audit.js` payload to gather information about the browser environment.

```bash
python3 ghost_cli.py audit --url https://example.com
```

### `lure` (Lure Foundry)
Create a variety of lure files for your authorized phishing campaigns.

**Create a QR Code:**
```bash
python3 ghost_cli.py lure --type qr_code --payload-url https://your-payload.com/beacon --output qr_lure.png
```

**Create a Shortened URL:**
```bash
python3 ghost_cli.py lure --type short_url --payload-url https://your-very-long-payload-url.com/beacon
```

**Create a JavaScript Dropper:**
```bash
python3 ghost_cli.py lure --type js_dropper --payload-url https://your-payload.com/payload.js --output dropper.js
```
