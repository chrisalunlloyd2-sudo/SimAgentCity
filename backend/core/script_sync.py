# TIMESTAMP: 2026-06-08T06:00:00Z
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: Gemini-CLI-Architect-LibrarySync

import os
import shutil
import json

class ScriptLibrarySync:
    """Synchronizes successful briefcase artifacts to ViperNotes."""
    def __init__(self, briefcase_dir, target_dir):
        self.briefcase_dir = briefcase_dir
        self.target_dir = target_dir

    def sync(self):
        """Scans briefcase, identifies high-fitness code, syncs to target."""
        print("[LIBRARY SYNC] Synchronizing successful patterns...")
        for filename in os.listdir(self.briefcase_dir):
            if filename.endswith(".json"):
                path = os.path.join(self.briefcase_dir, filename)
                with open(path, 'r') as f:
                    try:
                        data = json.load(f)
                        if data.get('fitness', 0) > 0.8: # Only sync high-fitness code
                            self._export(data['proposal'])
                    except: continue

    def _export(self, proposal):
        filename = f"optimized_{proposal.get('attemptId', 'unknown')}.py"
        target_path = os.path.join(self.target_dir, filename)
        with open(target_path, "w") as f:
            f.write(proposal.get('code', ''))
        print(f"[LIBRARY SYNC] Exported: {filename}")
