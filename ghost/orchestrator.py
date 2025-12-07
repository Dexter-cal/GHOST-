import os
import random
import string
from .mimic.engine import StealthEngine
from .identity.personality import PersonalityGenerator
from .browser.browser import CamouflageBrowser
from .behavior.walker import StepWalker
from .routing.router import MirageRouter
from .recon.scanner import ShadowScanner
from .reporting.garden import MemoryGarden
from .vault.vault import MemoryVault
from .payloads.casket import GhostCasket
from .delivery.courier import GhostCourier
from .listeners.link import GhostLink
from .shell.shell import GhostShell
from .ai.core import GhostAI
from .automation.account_creator import AccountAutomator
from .services.temp_email import TempEmailService

class GhostOrchestrator:
    """
    Orchestrator with missions for recon, account creation, and now, login.
    """
    def __init__(self):
        print("Orchestrator: Initializing Ghost systems...")
        vault_key = os.environ.get("GHOST_VAULT_KEY")
        if not vault_key:
            raise ValueError("GHOST_VAULT_KEY environment variable not set.")

        self.stealth_engine = StealthEngine()
        self.personality_generator = PersonalityGenerator()
        self.memory_garden = MemoryGarden(self.stealth_engine)
        self.vault = MemoryVault(vault_key.encode())
        self.payload_casket = GhostCasket()
        self.ghost_ai = GhostAI(self.stealth_engine)
        self.router = MirageRouter(self.stealth_engine, "config.json")
        self.shell = GhostShell(self.stealth_engine)
        self.listener = GhostLink(self.stealth_engine)
        self.temp_email_service = TempEmailService()
        print("Orchestrator: All systems online.")

    def _generate_random_string(self, length=12):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))

    def run_account_creation_mission(self, mission_params):
        # ... (previous mission logic remains the same) ...
        print("\n--- Starting Account Creation Mission ---")
        persona_id = mission_params.get("persona_id", "acct_creation_persona")
        target_domain = mission_params.get("target_domain")
        engagement_id = mission_params.get("engagement_id", "default_engagement")
        self.vault.create_engagement(engagement_id)
        persona = self.personality_generator.create_persona(persona_id)
        email = self.temp_email_service.get_temp_email()
        username = f"ghost_{self._generate_random_string(8)}"
        password = self._generate_random_string(16)
        browser = CamouflageBrowser(persona, self.stealth_engine)
        step_walker = StepWalker(browser.driver, persona, self.stealth_engine)
        automator = AccountAutomator(step_walker, browser)
        success = automator.run_signup_flow(target_domain, username, password, email)
        if success:
            self.memory_garden.log_event("Automation", f"Success creating account '{username}' on {target_domain}", "gusty (caution)")
            self.vault.store_credential(engagement_id, f"{username}_password", password)
            self.vault.store_credential(engagement_id, f"{username}_email", email)
        else:
            self.memory_garden.log_event("Alert", f"Failed to create account on {target_domain}", "thunderstorm (noisy)")
        self.memory_garden.render_garden()
        browser.close()
        print("--- Account Creation Mission Complete ---")

    def run_login_mission(self, mission_params):
        """
        A high-level method to execute a stealthy login mission.
        """
        print("\n--- Starting Login Mission ---")
        persona_id = mission_params.get("persona_id", "login_persona")
        target_domain = mission_params.get("target_domain")
        username = mission_params.get("username")
        engagement_id = mission_params.get("engagement_id")

        # 1. Retrieve Password from Vault
        password = self.vault.retrieve_credential(engagement_id, f"{username}_password")
        if not password:
            print(f"Error: Password for '{username}' not found in engagement '{engagement_id}'.")
            return

        # 2. Setup Browser and Automator
        persona = self.personality_generator.create_persona(persona_id)
        browser = CamouflageBrowser(persona, self.stealth_engine)
        step_walker = StepWalker(browser.driver, persona, self.stealth_engine)
        automator = AccountAutomator(step_walker, browser)
        self.memory_garden.log_event("Setup", f"Preparing to log in as '{username}'", "light drizzle (safe)")

        # 3. Execute Login Flow
        success = automator.run_login_flow(target_domain, username, password)
        if success:
            self.memory_garden.log_event("Automation", f"Successfully logged in as '{username}' on {target_domain}", "gusty (caution)")
        else:
            self.memory_garden.log_event("Alert", f"Failed to log in as '{username}' on {target_domain}", "thunderstorm (noisy)")

        # 4. For demonstration, we'll just wait. A real mission would continue here.
        print("Login successful. Browser will remain open for 10 seconds for verification.")
        time.sleep(10)

        self.memory_garden.render_garden()
        browser.close()
        print("--- Login Mission Complete ---")

    def create_and_run_mission(self, mission_params):
        # ... (previous mission logic remains the same) ...
        print("\n--- Starting New Mission ---")
        persona_id = mission_params.get("persona_id", "default_persona")
        target_host = mission_params.get("target_host")
        persona = self.personality_generator.create_persona(persona_id)
        browser = CamouflageBrowser(persona, self.stealth_engine)
        step_walker = StepWalker(browser.driver, persona, self.stealth_engine)
        scanner = ShadowScanner(self.stealth_engine, self.router)
        scanner.set_camouflage_profile("web_crawler")
        scanner.scan_for_common_paths(target_host, ["/admin", "/login", "/dashboard"])
        self.memory_garden.log_event("Recon", f"Scanned {target_host} for common paths", "gusty (caution)")
        self.ghost_ai.analyze_telemetry_for_profiling()
        alerts = self.stealth_engine.get_alerts()
        for alert in alerts:
            self.memory_garden.log_event("Alert", alert, "thunderstorm (noisy)")
        self.memory_garden.render_garden()
        browser.close()
        print("--- Mission Complete ---")
