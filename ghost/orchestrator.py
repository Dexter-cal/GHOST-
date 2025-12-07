import os
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

class GhostOrchestrator:
    """
    Initializes and connects all Ghost modules into a cohesive whole,
    providing a high-level API for performing complex operations.
    """
    def __init__(self):
        print("Orchestrator: Initializing Ghost systems...")

        # Securely load the vault key from an environment variable
        vault_key = os.environ.get("GHOST_VAULT_KEY")
        if not vault_key:
            raise ValueError("GHOST_VAULT_KEY environment variable not set. Cannot initialize vault.")

        self.stealth_engine = StealthEngine()
        self.personality_generator = PersonalityGenerator()
        self.memory_garden = MemoryGarden(self.stealth_engine)
        self.vault = MemoryVault(vault_key.encode()) # Key must be bytes
        self.payload_casket = GhostCasket()
        self.ghost_ai = GhostAI(self.stealth_engine)
        self.router = MirageRouter(self.stealth_engine, "config.json")
        self.shell = GhostShell(self.stealth_engine)
        self.listener = GhostLink(self.stealth_engine)
        print("Orchestrator: All systems online.")

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
