# TIMESTAMP: 2026-06-08T08:30:00Z
# PROJECT_ID: SimsMerged-v1.4.2
# AGENT_ID: Gemini-CLI-Architect-Master

import time
import os
import json
import datetime
import sys
import requests
import asyncio
from backend.core.message_bus import bus

# Sandbox handshake
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(root_dir)

from backend.core.hive_mind_router import HiveMindRouter
from backend.core.tester_node import TesterNode
from backend.core.critic_node import CriticNode
from backend.core.symphony_sync import SymphonySync
from backend.core.algebraic_governance import AlgebraicGovernance
class TaskPool:
    """Pre-allocated pool for task objects to avoid dynamic allocation."""
    def __init__(self, size=100):
        self.pool = [{"taskId": None, "goal": "", "context": "", "priority": 0} for _ in range(size)]
        self.index = 0

    def get_task(self, goal, context, priority):
        task = self.pool[self.index % len(self.pool)]
        task.update({"taskId": str(uuid.uuid4()), "goal": goal, "context": context, "priority": priority})
        self.index += 1
        return task

import time
import os
import json
import datetime
import sys
import requests
import asyncio
import shutil
from backend.core.message_bus import bus
from backend.core.hive_mind_router import HiveMindRouter
from backend.core.tester_node import TesterNode
from backend.core.critic_node import CriticNode
from backend.core.symphony_sync import SymphonySync
from backend.core.algebraic_governance import AlgebraicGovernance

class ActorObserverController:
    """Implements the Actor/Observer split and GITAUTOSHIP pattern."""
    def __init__(self):
        self.router = HiveMindRouter()
        self.tester = TesterNode(os.getcwd())
        self.critic = CriticNode()
        self.symphony = SymphonySync(os.getcwd())
        self.governor = AlgebraicGovernance()
        self.briefcase_dir = os.path.join(os.getcwd(), "briefcase")
        self.lib_dir = r"C:\Users\viper\OneDrive\Desktop\ViperNotes\src"
        self.chat_file = os.path.join(os.getcwd(), "chat_logs.json")
        self._observer_log("System", "ACTOR/OBSERVER INITIALIZED. GITAUTOSHIP READY.")

    def _observer_log(self, agent_name, message):
        """Observer: Logs activity and broadcasts to MSN chat bus."""
        entry = {
            "timestamp": datetime.datetime.now().strftime("%H:%M:%S"),
            "agent": agent_name,
            "message": message
        }
        # Archive
        logs = []
        if os.path.exists(self.chat_file):
            try:
                with open(self.chat_file, "r") as f:
                    logs = json.load(f)
            except: logs = []
        logs.append(entry)
        with open(self.chat_file, "w") as f:
            json.dump(logs[-100:], f, indent=2)

        # Broadcast (Active Observer)
        asyncio.run(bus.broadcast(entry))

    def _git_autoship(self, filename, content):
        """Git-Autoship: Add-only persistent library copy."""
        if not os.path.exists(self.lib_dir): os.makedirs(self.lib_dir)
        filepath = os.path.join(self.lib_dir, filename)
        with open(filepath, "w") as f:
            f.write(content)
        self._observer_log("GITAUTOSHIP", f"Committed to Library: {filename}")

    def run(self):
        print("[ACTOR] Processing tasks serially.")
        # ... (actor execution logic)

    def run(self):
        print("[MASTER CONTROLLER] Active.")
        
        while True:
            # Broadcast heartbeat
            self._log_to_chat("System", "HEARTBEAT_ACTIVE: Processing...")

            # 1. Harmonic throttle
            throttle_factor = self.governor.calculate_throttle()
            time.sleep(60 * throttle_factor)
            
            # 2. Symphony Sync
            self.symphony.run_symphony()
            
            # 3. Autonomous Minting (Phase 14)
            try:
                telemetry = requests.get("http://localhost:8000/api/machine-hardware-telemetry").json()
                mint_amount = telemetry['cpu_load'] * 0.5
                requests.post("http://localhost:8000/api/bank/mint", json={"amount": mint_amount})
                self._log_to_chat("Treasury", f"Minted {mint_amount:.2f} SPRITE based on load.")
            except Exception as e:
                self._log_to_chat("System", f"Minting error: {e}")
            
            # 4. Master Task
            if self.task_queue:
                task = self.task_queue.pop(0)
                self._log_to_chat("System", f"Processing: {task['goal']}")
                
                # Propose
                prompt = f"Goal: {task['goal']}. Context: {task['context']}. Output JSON: {{'attemptId': '{task['taskId']}', 'code': '...', 'rationale': '...'}}"
                proposal_raw = self.router.route_task(prompt, complexity="SMART")
                try:
                    proposal = json.loads(proposal_raw['response'])
                except: proposal = {"attemptId": task['taskId'], "code": "# ERR", "rationale": "Fail"}
                
                # Critique & Test
                critique = self.critic.analyze(proposal)
                test_results = self.tester.run_proposal(proposal)
                fitness = self.governor.calculate_throttle() 
                
                # Fitness check (Audit)
                if fitness < 0.5:
                    self._log_to_chat("System", f"Task {task['taskId']} rejected: Low predictive fitness ({fitness:.2f}).")
                    continue
                
                # Persist
                self._log_to_chat("Proposer", proposal['rationale'][:50])
                self._log_to_chat("Critic", critique['severity'])
                self._log_to_chat("Tester", str(test_results['pass_rate']))
                
                # archive
                with open(os.path.join(self.briefcase_dir, f"{task['taskId']}.json"), "w") as f:
                    json.dump({"proposal": proposal, "critique": critique, "test_results": test_results, "fitness": fitness}, f)

if __name__ == "__main__":
    controller = MasterController()
    controller.run()
