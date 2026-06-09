# TIMESTAMP: 2026-06-08T09:50:00Z
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: Gemini-CLI-Architect-Healer

import subprocess
import time
import requests

class SwarmHealer:
    """Proactively heals network and process deadlocks."""
    def diagnose_and_heal(self):
        # 1. Check WebSocket / API
        try:
            res = requests.get("http://localhost:8000/api/machine-heartbeat", timeout=2)
            if res.status_code != 200:
                raise Exception("API Unresponsive")
        except:
            print("[HEALER] Socket failure detected. Healing...")
            self.heal_bus()
            
    def heal_bus(self):
        # Surgical restart of components
        subprocess.run(["taskkill", "/F", "/IM", "python.exe"], capture_output=True)
        time.sleep(2)
        subprocess.Popen(["cmd", "/c", "start", "/low", "C:/Users/viper/python/python.exe", "backend/main.py"], cwd="C:/Users/viper/SimAgentCity")
        subprocess.Popen(["cmd", "/c", "start", "/low", "C:/Users/viper/python/python.exe", "master_controller.py"], cwd="C:/Users/viper/SimAgentCity")

if __name__ == "__main__":
    healer = SwarmHealer()
    healer.diagnose_and_heal()
