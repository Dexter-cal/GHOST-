import requests

class ShadowScanner:
    """
    Performs stealthy content discovery, now fully integrated with the
    MirageRouter to ensure all traffic is routed through the stealth stack.
    """
    def __init__(self, stealth_engine, router):
        self.stealth_engine = stealth_engine
        self.router = router
        self.discovered_paths = set()
        self.camouflage_profile = "web_crawler"

    def set_camouflage_profile(self, profile_name):
        """
        Sets the behavioral camouflage for the scanner.
        """
        self.camouflage_profile = profile_name

    def _get_camouflage_headers(self):
        """
        Returns a set of HTTP headers for a specific camouflage profile.
        """
        if self.camouflage_profile == "web_crawler":
            return { "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)" }
        elif self.camouflage_profile == "backup_agent":
            return { "User-Agent": "EnterpriseBackupClient/1.2.3" }
        return {}

    def scan_for_common_paths(self, host, paths_to_check):
        """
        Scans for common paths, routing all traffic through the MirageRouter.
        """
        print(f"ShadowScanner: Beginning scan of {host} via MirageRouter.")
        headers = self._get_camouflage_headers()

        for path in paths_to_check:
            url = f"https://{host}/{path.lstrip('/')}"
            proxy = self.router.get_exit_node()

            if not proxy:
                print("ShadowScanner: No healthy proxies available. Aborting scan.")
                break

            session = requests.Session()
            session.proxies = {"http": proxy, "https": proxy}

            try:
                response = session.get(url, headers=headers, timeout=10)
                self.stealth_engine.update_telemetry(host, response.elapsed.total_seconds(), success=response.ok)
                self.router.update_proxy_health(proxy, success=response.ok)

                if response.ok:
                    self.discovered_paths.add(path)
                    print(f"[+] Found: {url} (via {proxy})")

            except requests.RequestException as e:
                self.stealth_engine.update_telemetry(host, 10, success=False)
                self.router.update_proxy_health(proxy, success=False)
                print(f"[-] Error scanning {url} (via {proxy}): {e}")

            self.stealth_engine.wait(host)

        print("ShadowScanner: Scan complete.")
