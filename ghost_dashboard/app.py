from flask import Flask, render_template, jsonify
import os
import sys
from cryptography.fernet import Fernet

# Add the root project directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ghost.orchestrator import GhostOrchestrator

app = Flask(__name__)

# --- Initialize the real Ghost Orchestrator ---
orchestrator = None
try:
    key = os.environ.get("GHOST_VAULT_KEY")
    if not key:
        print("\n--- WARNING: GHOST_VAULT_KEY not set for dashboard! ---")
        print("Using a temporary, insecure key for this session only.")
        print("Set the environment variable for persistence.")
        print("-----------------------------------------------------\n")
        key = Fernet.generate_key().decode()
        os.environ["GHOST_VAULT_KEY"] = key

    orchestrator = GhostOrchestrator()
except Exception as e:
    print(f"FATAL: Could not initialize Ghost Orchestrator: {e}")


@app.route('/')
def index():
    """Serves the main dashboard page."""
    return render_template('index.html')

@app.route('/api/accounts/<engagement_id>')
def get_accounts(engagement_id):
    """API endpoint to get a list of accounts for an engagement."""
    if not orchestrator:
        return jsonify({"error": "Orchestrator not initialized."}), 500

    accounts = orchestrator.vault.list_accounts_in_engagement(engagement_id)
    account_details = {}
    for acc in accounts:
        account_details[acc] = {
            "email": orchestrator.vault.retrieve_account_data(engagement_id, acc, "email"),
            "status": "active", # Placeholder for now
        }
    return jsonify(account_details)


def run_dashboard():
    app.run(port=5555, debug=True)

if __name__ == '__main__':
    run_dashboard()
