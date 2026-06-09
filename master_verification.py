# TIMESTAMP: 2026-06-08T09:45:00Z
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: Gemini-CLI-Architect-Auditor

import requests
import json
import time

class MasterVerifier:
    """Verifies full system integrity."""
    def __init__(self):
        self.endpoints = {
            "Heartbeat": "http://localhost:8000/api/machine-heartbeat",
            "Chat": "http://localhost:8000/chat",
            "Metropolis": "http://localhost:8000/api/metropolis-state",
            "Hardware": "http://localhost:8000/api/machine-hardware-telemetry"
        }

    def verify(self):
        print("[AUDIT] Starting Full Stack Verification...")
        results = {}
        for name, url in self.endpoints.items():
            try:
                res = requests.get(url, timeout=5)
                results[name] = res.status_code == 200
                print(f"[AUDIT] {name}: {'PASS' if results[name] else 'FAIL'}")
            except Exception as e:
                results[name] = False
                print(f"[AUDIT] {name}: FAIL ({e})")
        
        return results

if __name__ == "__main__":
    verifier = MasterVerifier()
    res = verifier.verify()
    if all(res.values()):
        print("[AUDIT] FULL SYSTEM INTEGRITY: PASS")
    else:
        print("[AUDIT] FULL SYSTEM INTEGRITY: FAIL")
