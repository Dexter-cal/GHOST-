import os
import random
import string
import time
from .mimic.engine import StealthEngine
from .identity.personality import PersonalityGenerator
from .identity.lifecycle import LifecycleManager, PersonaState
from .identity.passwords import PasswordGenerator
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
    Orchestrator with enhanced identity generation integrated into missions.
    """
    def __init__(self):
        # ... (previous __init__ logic is the same) ...
        vault_key = os.environ.get("GHOST_VAULT_KEY")
        if not vault_key: raise ValueError("GHOST_VAULT_KEY not set.")
        self.stealth_engine = StealthEngine()
        self.personality_generator = PersonalityGenerator()
        self.password_generator = PasswordGenerator()
        self.memory_garden = MemoryGarden(self.stealth_engine)
        self.vault = MemoryVault(vault_key.encode())
        self.lifecycle_manager = LifecycleManager(self.vault)
        self.payload_casket = GhostCasket()
        self.ghost_ai = GhostAI(self.stealth_engine)
        self.router = MirageRouter(self.stealth_engine, "config.json")
        self.shell = GhostShell(self.stealth_engine)
        self.listener = GhostLink(self.stealth_engine)
        self.temp_email_service = TempEmailService()
        print("Orchestrator: All systems online.")

    def run_account_creation_mission(self, mission_params):
        """
        Runs the account creation mission using the new enhanced identity
        and password generation capabilities.
        """
        print("\n--- Starting Enhanced Account Creation Mission ---")
        persona_id = mission_params.get("persona_id", "acct_creation_persona")
        target_domain = mission_params.get("target_domain")
        engagement_id = mission_params.get("engagement_id")
        password_strategy = mission_params.get("password_strategy", "random")

        # 1. Create Full Persona
        self.vault.create_engagement(engagement_id)
        persona = self.personality_generator.create_persona(persona_id)
        self.lifecycle_manager.update_persona_state(engagement_id, persona, PersonaState.NEW)
        self.vault.store_persona(engagement_id, persona)

        # 2. Select Username and Generate Password
        username = random.choice(persona["identity"]["potential_usernames"])
        password = self.password_generator.generate_password(strategy=password_strategy)
        email = self.temp_email_service.get_temp_email()

        self.memory_garden.log_event("Identity", f"Generated identity {username} ({persona['identity']['first_name']})", "safe")

        # 3. Execute Signup Flow
        browser = CamouflageBrowser(persona, self.stealth_engine)
        step_walker = StepWalker(browser.driver, persona, self.stealth_engine)
        automator = AccountAutomator(step_walker, browser)
        success = automator.run_signup_flow(target_domain, username, password, email)

        # 4. Store Credentials and Update State
        if success:
            self.memory_garden.log_event("Automation", f"Success creating account '{username}'", "caution")
            self.vault.store_credential(engagement_id, f"{username}_password", password)
            self.vault.store_credential(engagement_id, f"{username}_email", email)
            self.lifecycle_manager.update_persona_state(engagement_id, persona, PersonaState.ACTIVE)
        else:
            self.memory_garden.log_event("Alert", f"Failed to create account on {target_domain}", "noisy")

        self.memory_garden.render_garden()
        browser.close()
        print("--- Account Creation Mission Complete ---")

    # ... (Other missions like run_login_mission and create_and_run_mission remain the same) ...
    def run_login_mission(self, mission_params):
        print("\n--- Starting Login Mission ---")
        persona_id = mission_params.get("persona_id", "login_persona")
        target_domain = mission_params.get("target_domain")
        username = mission_params.get("username")
        engagement_id = mission_params.get("engagement_id")
        password = self.vault.retrieve_credential(engagement_id, f"{username}_password")
        if not password:
            print(f"Error: Password for '{username}' not found in engagement '{engagement_id}'.")
            return
        persona = self.vault.retrieve_persona(engagement_id, username)
        if not persona:
            persona = self.personality_generator.create_persona(persona_id)
        browser = CamouflageBrowser(persona, self.stealth_engine)
        step_walker = StepWalker(browser.driver, persona, self.stealth_engine)
        automator = AccountAutomator(step_walker, browser)
        self.memory_garden.log_event("Setup", f"Preparing to log in as '{username}'", "light drizzle (safe)")
        success = automator.run_login_flow(target_domain, username, password)
        if success:
            self.memory_garden.log_event("Automation", f"Successfully logged in as '{username}' on {target_domain}", "gusty (caution)")
        else:
            self.memory_garden.log_event("Alert", f"Failed to log in as '{username}' on {target_domain}", "thunderstorm (noisy)")
        print("Login successful. Browser will remain open for 10 seconds for verification.")
        time.sleep(10)
        self.memory_garden.render_garden()
        browser.close()
        print("--- Login Mission Complete ---")

    def run_persona_warmup_mission(self, mission_params):
        """
        Guides a persona through a series of subtle, history-building actions.
        """
        print("\n--- Starting Persona Warm-Up Mission ---")
        engagement_id = mission_params.get("engagement_id")
        persona_id = mission_params.get("persona_id")
        target_domain = mission_params.get("target_domain")

        # 1. Retrieve the persona
        persona = self.vault.retrieve_persona(engagement_id, persona_id)
        if not persona:
            print(f"Error: Persona '{persona_id}' not found in engagement '{engagement_id}'.")
            return

        self.lifecycle_manager.update_persona_state(engagement_id, persona, PersonaState.WARMING_UP)
        self.memory_garden.log_event("Lifecycle", f"Starting warm-up for persona '{persona_id}'", "light drizzle (safe)")

        # 2. Perform a simple, harmless action (e.g., visit homepage)
        browser = CamouflageBrowser(persona, self.stealth_engine)
        print(f"Warm-Up: Visiting https://{target_domain} to establish presence...")
        browser.get(f"https://{target_domain}", target_domain)
        time.sleep(random.uniform(3, 7)) # Simulate reading the page
        browser.close()

        self.memory_garden.log_event("Warm-Up", f"Visited homepage of {target_domain}", "light drizzle (safe)")

        # 3. Collapse the persona to simulate inactivity
        self.lifecycle_manager.update_persona_state(engagement_id, persona, PersonaState.COLLAPSED)
        collapse_duration_hours = random.uniform(4, 12)
        print(f"Warm-Up: Persona '{persona_id}' is now collapsing for approximately {collapse_duration_hours:.1f} hours.")

        self.memory_garden.render_garden()
        print("--- Persona Warm-Up Mission Complete ---")

    def create_and_run_mission(self, mission_params):
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
