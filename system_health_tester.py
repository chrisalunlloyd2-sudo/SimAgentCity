# TIMESTAMP: 2026-06-08T04:30:00Z
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: Gemini-CLI-Architect-Tester

import requests
import time
import subprocess
import os

class SystemHealthTester:
    def __init__(self):
        self.endpoints = ["http://localhost:8000/api/machine-heartbeat", "http://localhost:8000/chat"]
        self.successes = 0
        self.failures = 0
        self.max_cycles = 10

    def test_cycle(self):
        print(f"[TESTER] Cycle {self.successes + self.failures + 1}/{self.max_cycles}")
        all_passed = True
        for url in self.endpoints:
            try:
                response = requests.get(url, timeout=5)
                if response.status_code != 200:
                    print(f"[TESTER] Endpoint {url} returned {response.status_code}")
                    all_passed = False
            except Exception as e:
                print(f"[TESTER] Endpoint {url} failed: {e}")
                all_passed = False
        
        if all_passed:
            self.successes += 1
            print("[TESTER] Cycle PASSED.")
        else:
            self.failures += 1
            print("[TESTER] Cycle FAILED. Restarting backend...")
            self.restart_backend()
            
    def restart_backend(self):
        # Force restart
        subprocess.run(["taskkill", "/F", "/IM", "python.exe"], capture_output=True)
        time.sleep(5) # Give it time to release port
        subprocess.Popen(["cmd", "/c", "start", "/low", "C:/Users/viper/python/python.exe", "backend/main.py"], cwd="C:/Users/viper/SimAgentCity")
        time.sleep(15) # Wait longer for FastAPI to bind

    def run(self):
        for _ in range(self.max_cycles):
            self.test_cycle()
            time.sleep(5)
        print(f"[TESTER] Final Results: {self.successes} Passed, {self.failures} Failed.")

if __name__ == "__main__":
    tester = SystemHealthTester()
    tester.run()
