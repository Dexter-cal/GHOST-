import json
import os
import time
from selenium.webdriver.common.by import By

class AccountCreator:
    """
    Orchestrates the process of creating an account on a website,
    using a StepWalker for human-like interaction and site-specific rules
    from a JSON file.
    """
    def __init__(self, step_walker, browser, rules_path="site_rules.json"):
        self.step_walker = step_walker
        self.browser = browser
        self.rules_path = rules_path
        self.rules = self._load_rules()

    def _load_rules(self):
        """
        Loads the site rules from the specified JSON file.
        """
        if not os.path.exists(self.rules_path):
            print(f"Warning: Site rules file not found at '{self.rules_path}'. Account creation will fail.")
            return {}
        try:
            with open(self.rules_path, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Could not decode JSON from '{self.rules_path}'.")
            return {}

    def _find_element(self, by, value):
        """
        Finds an element on the page using the specified locator strategy.
        """
        locator_map = {
            "id": By.ID,
            "name": By.NAME,
            "css": By.CSS_SELECTOR,
            "xpath": By.XPATH,
        }
        if by not in locator_map:
            raise ValueError(f"Unsupported locator strategy: {by}")

        return self.browser.driver.find_element(locator_map[by], value)

    def create_account(self, domain, username, password, email):
        """
        Attempts to create an account for a given domain using the loaded rules.
        """
        if domain not in self.rules:
            print(f"Error: No site rules found for domain '{domain}'.")
            return False

        rule = self.rules[domain]
        print(f"AccountCreator: Starting account creation for '{domain}'...")

        try:
            # 1. Navigate to the signup page
            self.browser.get(rule["signup_url"], domain)

            # 2. Fill in the fields
            for field_name, locator in rule["fields"].items():
                element = self._find_element(locator["by"], locator["value"])

                if field_name == "username":
                    self.step_walker.human_like_typing(element, username)
                elif field_name == "email":
                    self.step_walker.human_like_typing(element, email)
                elif field_name == "password":
                    self.step_walker.human_like_typing(element, password)
                # Extend with more field types as needed

            # 3. Click the submit button
            submit_locator = rule["submit_button"]
            submit_button = self._find_element(submit_locator["by"], submit_locator["value"])
            self.step_walker.human_like_click(submit_button)

            # 4. Wait after submission
            wait_time = rule.get("post_submit_wait_seconds", 5)
            print(f"AccountCreator: Form submitted. Waiting for {wait_time} seconds...")
            time.sleep(wait_time)

            print("AccountCreator: Account creation process completed successfully.")
            return True

        except Exception as e:
            print(f"An error occurred during account creation for {domain}: {e}")
            return False
