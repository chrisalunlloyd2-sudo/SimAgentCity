# TIMESTAMP: 2026-06-07T16:40:00Z
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: Gemini-CLI-Architect

import json
import os
import uuid
import time
from backend.core.hive_mind_router import HiveMindRouter
from backend.core.tester_node import TesterNode
from backend.core.critic_node import CriticNode
from backend.core.symphony_sync import SymphonySync
from backend.core.algebraic_governance import AlgebraicGovernance

# Phase 5: Serial Orchestrator (Refactored for Symphonic-Chain)
class RingOrchestrator:
    def __init__(self):
        self.task_queue = [] 
        self.router = HiveMindRouter()
        self.tester = TesterNode(os.getcwd())
        self.critic = CriticNode()
        self.symphony = SymphonySync(os.getcwd())
        self.governor = AlgebraicGovernance()
        self.briefcase_dir = os.path.join(os.getcwd(), "briefcase")
        print("[RING ORCHESTRATOR] Initialized. Symphonic mode: SERIAL.")

    def submit_task(self, goal, constraints, context, priority=1):
        """Adds to the master list. Enforces serial bottleneck."""
        task = {
            "taskId": str(uuid.uuid4()),
            "goal": goal,
            "constraints": constraints,
            "context": context,
            "priority": priority
        }
        self.task_queue.append(task)
        return task["taskId"]

    def _log_to_chat(self, agent_name, message):
        """Append to chat log for UI visibility."""
        log_file = "chat_logs.json"
        entry = {
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "agent": agent_name,
            "message": message
        }
        logs = []
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                try: logs = json.load(f)
                except: logs = []
        logs.append(entry)
        with open(log_file, "w") as f:
            json.dump(logs[-100:], f, indent=2)

    def run_continuous(self):
        """Continuous serial background execution loop."""
        print("[RING ORCHESTRATOR] Serial loop started.")
        while True:
            throttle_factor = self.governor.calculate_throttle()
            time.sleep(60 * throttle_factor) 
            
            if not self.task_queue:
                continue

            task = self.task_queue.pop(0)
            self._log_to_chat("System", f"Starting task: {task['goal']}")
            
            # PROPOSER ROLE
            prompt = f"Goal: {task['goal']}. Context: {task['context']}. Output ONLY valid JSON: {{'attemptId': '{task['taskId']}', 'code': '...', 'rationale': '...'}}"
            proposal_raw = self.router.route_task(prompt, complexity="SMART")
            try:
                proposal = json.loads(proposal_raw['response'])
                self._log_to_chat("Proposer", f"Proposed code for {task['taskId']}: {proposal['rationale']}")
            except:
                proposal = {"attemptId": task['taskId'], "code": "# ERROR", "rationale": "Parsing failed"}
                self._log_to_chat("Proposer", "Failed to parse code.")
                
            # CRITIC ROLE
            critique = self.critic.analyze(proposal)
            self._log_to_chat("Critic", f"Severity: {critique['severity']} - {critique['issue']}")
            
            # TESTER ROLE
            test_results = self.tester.run_proposal(proposal)
            self._log_to_chat("Tester", f"Pass rate: {test_results['pass_rate']}")
            
            # ARCHIVE (Add-only)
            result_data = {"proposal": proposal, "critique": critique, "test_results": test_results}
            filepath = os.path.join(self.briefcase_dir, f"{task['taskId']}.json")
            with open(filepath, "w") as f:
                json.dump(result_data, f, indent=2)
            
            self._log_to_chat("System", f"Task {task['taskId']} persisted.")
            print(f"[RING ORCHESTRATOR] Task {task['taskId']} critiqued, tested, and persisted.")

if __name__ == "__main__":
    orch = RingOrchestrator()
    # Continuous objective: finish the Isometric Game UI
    orch.submit_task("Implement Isometric Tile Rendering", {"language": "js", "safety": "loose"}, "Focus on engine.js and city-canvas.")
    orch.run_continuous()
