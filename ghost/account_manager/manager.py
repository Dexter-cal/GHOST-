from ghost.browser.browser import CamouflageBrowser

class AccountManager:
    """
    The central control panel for managing Ghost identities, now with a
    fully functional "Session Teleporter."
    """
    def __init__(self, vault, orchestrator):
        self.vault = vault
        self.orchestrator = orchestrator
        print("AccountManager: Initialized.")

    def list_accounts(self, engagement_id):
        """Provides a dashboard view of all accounts."""
        print(f"AccountManager: Listing accounts for engagement '{engagement_id}'...")
        accounts = self.vault.list_accounts_in_engagement(engagement_id)
        # In a real UI, you'd show more details.
        return accounts

    def launch_session(self, engagement_id, username, domain):
        """
        The "Session Teleporter." Launches a browser and injects the
        session for a given account to bypass login.
        """
        print(f"AccountManager: Launching session for '{username}' on '{domain}'...")

        # 1. Retrieve session data from the vault
        cookies = self.vault.retrieve_account_data(engagement_id, username, "cookies")
        persona_id = self.vault.retrieve_account_data(engagement_id, username, "persona_id")

        if not cookies or not persona_id:
            print("Error: No session cookies or persona found for this account. Please log in normally first to capture a session.")
            return

        persona = self.vault.retrieve_persona(engagement_id, persona_id)
        if not persona:
            print(f"Error: Persona '{persona_id}' not found.")
            return

        # 2. Launch a new browser
        # Note: For cookie injection to work, the browser must first navigate to the domain.
        browser = CamouflageBrowser(persona, self.orchestrator.stealth_engine)
        browser.get(f"https://{domain}", domain)

        # 3. Inject the cookies
        browser.inject_cookies(cookies)

        # 4. Navigate to the dashboard (or refresh the page)
        print("Session Teleporter: Cookies injected. Refreshing page to enter session...")
        browser.get(f"https://{domain}", domain)

        print("Session Teleporter: Session launched! The browser will remain open until you close it.")
        # The user is now in control of the browser session.
        # We will wait for them to close it.
        try:
            while True:
                # This is a simple way to keep the script alive
                # while the user interacts with the browser.
                import time
                time.sleep(1)
                # Check if the browser is still alive
                if not browser.driver.window_handles:
                    break
        except Exception:
            # Browser was likely closed
            pass
        finally:
            print("Session Teleporter: Browser closed. Mission complete.")
            browser.close()

    def delete_account(self, engagement_id, username, domain):
        # ... (Placeholder)
        pass
