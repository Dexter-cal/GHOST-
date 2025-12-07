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
from .automation.account_creator import AccountCreator
from .services.temp_email import TempEmailService

class GhostOrchestrator:
    """
    Initializes and connects all Ghost modules, now with a dedicated mission
    for stealthy account creation.
    """
    def __init__(self):
        print("Orchestrator: Initializing Ghost systems...")
        # ... (previous __init__ logic remains the same) ...
        vault_key = os.environ.get("GHOST_VAULT_KEY")
        if not vault_key:
            raise ValueError("GHOST_VAULT_KEY environment variable not set. Cannot initialize vault.")

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
        """Generates a random string for usernames and passwords."""
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    def run_account_creation_mission(self, mission_params):
        """
        A high-level method to execute a stealthy account creation mission.
        """
        print("\n--- Starting Account Creation Mission ---")
        persona_id = mission_params.get("persona_id", "acct_creation_persona")
        target_domain = mission_params.get("target_domain")
        engagement_id = mission_params.get("engagement_id", "default_engagement")

        # 1. Create Persona and Engagement Vault
        persona = self.personality_generator.create_persona(persona_id)
        self.vault.create_engagement(engagement_id)
        self.memory_garden.log_event("Setup", f"Created persona '{persona_id}' for engagement '{engagement_id}'", "light drizzle (safe)")

        # 2. Get Temporary Email
        email = self.temp_email_service.get_temp_email()
        self.memory_garden.log_event("Setup", f"Acquired temporary email: {email}", "light drizzle (safe)")

        # 3. Generate Credentials
        username = f"ghost_{self._generate_random_string(8)}"
        password = self._generate_random_string(16)

        # 4. Setup Browser and Account Creator
        browser = CamouflageBrowser(persona, self.stealth_engine)
        step_walker = StepWalker(browser.driver, persona, self.stealth_engine)
        account_creator = AccountCreator(step_walker, browser)

        # 5. Execute Account Creation
        success = account_creator.create_account(target_domain, username, password, email)

        # 6. Store Credentials and Report
        if success:
            self.memory_garden.log_event("Automation", f"Successfully created account '{username}' on {target_domain}", "gusty (caution)")
            self.vault.store_credential(engagement_id, f"{username}_password", password)
            self.vault.store_credential(engagement_id, f"{username}_email", email)
            print(f"Credentials for '{username}' securely stored in vault under engagement '{engagement_id}'.")
        else:
            self.memory_garden.log_event("Alert", f"Failed to create account on {target_domain}", "thunderstorm (noisy)")

        # 7. Render Final Report and Cleanup
        self.memory_garden.render_garden()
        browser.close()
        print("--- Account Creation Mission Complete ---")

    def create_and_run_mission(self, mission_params):
        """
        A high-level method to execute a full mission.
        """
        print("\n--- Starting New Mission ---")
        persona_id = mission_params.get("persona_id", "default_persona")
        target_host = mission_params.get("target_host")

        # 1. Create Persona
        persona = self.personality_generator.create_persona(persona_id)
        self.memory_garden.log_event("Persona", f"Created persona '{persona_id}'", "light drizzle (safe)")

        # 2. Setup Browser
        browser = CamouflageBrowser(persona, self.stealth_engine)
        step_walker = StepWalker(browser.driver, persona, self.stealth_engine)

        # 3. Perform Recon
        scanner = ShadowScanner(self.stealth_engine, self.router)
        scanner.set_camouflage_profile("web_crawler")
        scanner.scan_for_common_paths(target_host, ["/admin", "/login", "/dashboard"])
        self.memory_garden.log_event("Recon", f"Scanned {target_host} for common paths", "gusty (caution)")

        # 4. Analyze and Report
        self.ghost_ai.analyze_telemetry_for_profiling()
        alerts = self.stealth_engine.get_alerts()
        for alert in alerts:
            self.memory_garden.log_event("Alert", alert, "thunderstorm (noisy)")

        # 5. Render Final Report
        self.memory_garden.render_garden()

        # 6. Cleanup
        browser.close()
        print("--- Mission Complete ---")
