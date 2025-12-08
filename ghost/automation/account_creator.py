import json
import os
import time
from selenium.webdriver.common.by import By

class AccountAutomator:
    """
    Orchestrates automated interactions, now with a new flow for
    automated account deletion.
    """
    def __init__(self, step_walker, browser, rules_path="site_rules.json"):
        # ... (same as before) ...
        self.step_walker = step_walker
        self.browser = browser
        self.rules_path = rules_path
        self.rules = self._load_rules()

    # ... ( _load_rules, _find_element, _handle_captcha are the same) ...

    def run_account_deletion_flow(self, domain, username):
        """Runs the account deletion flow for a given domain."""
        rule = self.rules.get(domain)
        if not rule:
            print(f"Error: No site rules found for domain '{domain}'.")
            return False

        print(f"Automator: Starting account deletion for '{username}' on '{domain}'...")
        try:
            # First, we must log in to access the account settings page.
            # This assumes a login has just occurred.

            self.browser.get(rule["account_deletion_url"], domain)

            # Fill in confirmation field if it exists
            if "account_deletion_confirmation_field" in rule:
                conf_loc = rule["account_deletion_confirmation_field"]
                conf_field = self._find_element(conf_loc["by"], conf_loc["value"])
                # The confirmation often requires typing the username
                self.step_walker.human_like_typing(conf_field, username)

            # Click the final delete button
            del_loc = rule["account_deletion_submit_button"]
            del_button = self._find_element(del_loc["by"], del_loc["value"])
            self.step_walker.human_like_click(del_button)

            print("Automator: Account deletion submitted.")
            time.sleep(rule.get("post_submit_wait_seconds", 5))
            return True

        except Exception as e:
            print(f"An error occurred during account deletion for {domain}: {e}")
            return False

    # ... (signup and login flows remain the same) ...
    def _load_rules(self):
        """Loads the site rules from the specified JSON file."""
        if not os.path.exists(self.rules_path):
            print(f"Warning: Site rules not found at '{self.rules_path}'.")
            return {}
        try:
            with open(self.rules_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from '{self.rules_path}'.")
            return {}

    def _find_element(self, by, value):
        """Finds an element on the page."""
        locator_map = {"id": By.ID, "name": By.NAME, "css": By.CSS_SELECTOR, "xpath": By.XPATH}
        if by not in locator_map:
            raise ValueError(f"Unsupported locator strategy: {by}")
        return self.browser.driver.find_element(locator_map[by], value)

    def run_signup_flow(self, domain, username, password, email):
        """Runs the account creation (signup) flow for a given domain."""
        rule = self.rules.get(domain)
        if not rule:
            print(f"Error: No site rules found for domain '{domain}'.")
            return False
        print(f"Automator: Starting signup for '{domain}'...")
        try:
            self.browser.get(rule["signup_url"], domain)
            for field_name, locator in rule["signup_fields"].items():
                element = self._find_element(locator["by"], locator["value"])
                if field_name == "username": self.step_walker.human_like_typing(element, username)
                elif field_name == "email": self.step_walker.human_like_typing(element, email)
                elif field_name == "password": self.step_walker.human_like_typing(element, password)

            submit_locator = rule["signup_submit_button"]
            submit_button = self._find_element(submit_locator["by"], submit_locator["value"])
            self.step_walker.human_like_click(submit_button)

            wait_time = rule.get("post_submit_wait_seconds", 5)
            print(f"Automator: Signup form submitted. Waiting {wait_time}s...")
            time.sleep(wait_time)
            print("Automator: Signup flow completed successfully.")
            return True
        except Exception as e:
            print(f"An error occurred during signup for {domain}: {e}")
            return False

    def run_login_flow(self, domain, username, password):
        """Runs the login flow for a given domain."""
        rule = self.rules.get(domain)
        if not rule:
            print(f"Error: No site rules found for domain '{domain}'.")
            return False
        print(f"Automator: Starting login for '{username}' on '{domain}'...")
        try:
            self.browser.get(rule["login_url"], domain)
            for field_name, locator in rule["login_fields"].items():
                element = self._find_element(locator["by"], locator["value"])
                if field_name == "username": self.step_walker.human_like_typing(element, username)
                elif field_name == "password": self.step_walker.human_like_typing(element, password)

            submit_locator = rule["login_submit_button"]
            submit_button = self._find_element(submit_locator["by"], submit_locator["value"])
            self.step_walker.human_like_click(submit_button)

            wait_time = rule.get("post_submit_wait_seconds", 5)
            print(f"Automator: Login form submitted. Waiting {wait_time}s...")
            time.sleep(wait_time)
            print("Automator: Login flow completed successfully.")
            return True
        except Exception as e:
            print(f"An error occurred during login for {domain}: {e}")
            return False
