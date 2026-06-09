# TIMESTAMP: 2026-06-08T01:30:00Z
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: Gemini-CLI-Architect-Critic

import json
from backend.core.hive_mind_router import HiveMindRouter

class CriticNode:
    """Phase 13: Structural and Logic Criticism Node."""
    def __init__(self):
        self.router = HiveMindRouter()

    def analyze(self, proposal):
        """Analyzes code proposal for flaws."""
        code = proposal.get("code", "")
        prompt = f"Critique this code for logic errors, security risks, and style. Output ONLY valid JSON: {{'issue': '...', 'location': '...', 'severity': 'HIGH|MEDIUM|LOW'}}. Code: {code}"
        
        critique_raw = self.router.route_task(prompt, complexity="SMART")
        
        try:
            return json.loads(critique_raw['response'])
        except:
            return {"issue": "Parsing failed", "location": "N/A", "severity": "LOW"}
