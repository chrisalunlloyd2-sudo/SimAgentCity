# TIMESTAMP: 2026-06-08T09:30:00Z
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: Gemini-CLI-Architect-Watchdog

import subprocess
import time
import psutil

class StabilityWatchdog:
    """Proactively monitors backend and controller PIDs."""
    def __init__(self, components):
        self.components = components # Dict of {name: command}

    def check_and_heal(self):
        for name, cmd in self.components.items():
            if not self.is_running(name):
                print(f"[WATCHDOG] Healing {name}...")
                subprocess.Popen(cmd, shell=True)
                time.sleep(5)

    def is_running(self, name):
        for proc in psutil.process_iter(['name', 'cmdline']):
            if name in str(proc.info['cmdline']):
                return True
        return False

if __name__ == "__main__":
    components = {
        "main.py": "start /low C:/Users/viper/python/python.exe backend/main.py",
        "master_controller.py": "start /low C:/Users/viper/python/python.exe master_controller.py"
    }
    watchdog = StabilityWatchdog(components)
    while True:
        watchdog.check_and_heal()
        time.sleep(10)
