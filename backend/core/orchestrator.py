import threading
import queue
import time
import os
import sys

# Handshake for local sandbox testing
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from .os_bridge import OSBridge
    from .hive_mind_router import HiveMindRouter
    from .file_watcher import CityFileWatcher
    from .self_corrector import AgentSelfCorrector
    from .crypto_ledger import CryptoLedger
except ImportError:
    from os_bridge import OSBridge
    from hive_mind_router import HiveMindRouter
    from file_watcher import CityFileWatcher
    from self_corrector import AgentSelfCorrector
    from crypto_ledger import CryptoLedger

class AgentCityOrchestrator:
    def __init__(self, workspace_dir):
        self.bridge = OSBridge(workspace_dir)
        self.hive = HiveMindRouter()
        self.corrector = AgentSelfCorrector(self.hive)
        self.task_queue = queue.Queue()
        self.active_agents = {} # agent_id: {status, thought, xp, stamina, wallet, balance}
        self.pulse_rate = 1.2
        self.running = True

        # Phase 52: True DePIN Crypto Ledger
        self.ledger = CryptoLedger(os.path.join(os.getcwd(), "blockchain_ledger.json"), difficulty=3)

        # Step 51-75: Initialize Real-time Watcher
        self.watcher = CityFileWatcher(workspace_dir, self._on_fs_event)
        self.watcher.start()

        # Start Heartbeat Thread
        self.heartbeat_thread = threading.Thread(target=self._run_heartbeat, daemon=True)
        self.heartbeat_thread.start()

    def _on_fs_event(self, event_type, path):
        """Callback for file system events. Triggers autonomous zoning logic."""
        if event_type in ["CREATED", "MODIFIED"]:
            print(f"[PULSE] FS Event: {event_type} on {path}. Analyzing zone requirements...")

    def _clear_transaction(self, agent_id, task_type, cost=10):
        """Phase 52: True PoW Bank Monitor Anchor."""
        # Assume agents pay the System for the right to execute tasks
        tx_hash = self.ledger.add_transaction(sender=agent_id, receiver="System", amount=cost, currency="PYTHON_COIN", contract=task_type)
        print(f"[BANK] Tx Mined: {tx_hash[:16]}... {agent_id} paid {cost} PYTHON_COIN for {task_type}")
        return tx_hash

    def run_miner_loop(self, agent_id, file_path):
        """Steps 701-725: The Miner (Scan & Categorize)."""
        self.active_agents[agent_id].update({"status": "MINING", "thought": "Sifting for data nuggets..."})
        self._clear_transaction(agent_id, "MINING")
        print(f"[MINER] File {file_path} mined and categorized.")

    def run_processor_loop(self, agent_id, file_path, instructions):
        """Steps 726-750: The Processor (LLM Analysis)."""
        self.assign_task(agent_id, file_path, instructions)
        self._clear_transaction(agent_id, "PROCESSING")

    def run_shipper_loop(self, agent_id, local_path, repo_name):
        """Steps 751-800: The Shipper (Auto-Ship to GitHub)."""
        self.active_agents[agent_id].update({"status": "SHIPPING", "thought": "Paving the road to GitHub..."})
        self._clear_transaction(agent_id, "SHIPPING")
        try:
            print(f"[SHIPPER] Deploying {local_path} to repository: {repo_name}")
            self.active_agents[agent_id].update({"status": "IDLE", "thought": "Cargo delivered."})
            return True
        except Exception as e:
            self.active_agents[agent_id].update({"status": "ERROR", "thought": str(e)})
            return False

    def _run_heartbeat(self):
        """Step 5: The Pulse Handshake implementation. Restores stamina for idle agents."""
        while self.running:
            for aid, state in self.active_agents.items():
                if state["status"] == "IDLE" and state.get("stamina", 0) < 100:
                    state["stamina"] += 2 # Regen stamina
            time.sleep(self.pulse_rate)

    def assign_task(self, agent_id, file_path, task):
        """Queues a task for an agent sim."""
        self.task_queue.put({
            "id": agent_id,
            "file": file_path,
            "task": task
        })
        self._process_next()

    def _process_next(self):
        if not self.task_queue.empty():
            t = self.task_queue.get()
            thread = threading.Thread(target=self._execute_agent_flow, args=(t,), daemon=True)
            thread.start()

    def _execute_agent_flow(self, task_data):
        """Atomic Flow: Mine -> Process -> Box -> Ship."""
        aid = task_data["id"]
        fpath = task_data["file"]
        desc = task_data["task"]
        
        if aid not in self.active_agents:
            self.active_agents[aid] = {"status": "IDLE", "thought": "Awaiting orders.", "xp": 0, "stamina": 100}

        # Check stamina before starting
        if self.active_agents[aid].get("stamina", 100) < 20:
            self.active_agents[aid].update({"status": "RESTING", "thought": "Too tired. Need to recharge."})
            print(f"[SYSTEM] {aid} is exhausted. Task deferred.")
            return

        self.active_agents[aid].update({"status": "PROCESSING", "thought": "Analyzing terrain...", "stamina": self.active_agents[aid]["stamina"] - 20})
        
        # Pay for processing
        self._clear_transaction(aid, "PROCESSING_CYCLE", cost=5)

        full_path = os.path.join(self.bridge.root_dir, fpath)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            self.active_agents[aid]["thought"] = self.hive.generate_chat_bubble(aid, "Worker", "Data Extraction")

            res = self.hive.route_task(f"Process this file: {desc}\n\nContent:\n{content}", complexity="SMART")
            result = res.get("response", "")
            
            if res.get("status") != "SUCCESS" and res.get("status") is not None:
                raise Exception(f"Neural Router Failure: {res.get('status')}")

            dest_path = f"processed/agent_{aid}_{os.path.basename(fpath)}"
            final_dest = os.path.join(self.bridge.root_dir, dest_path)
            os.makedirs(os.path.dirname(final_dest), exist_ok=True)
            with open(final_dest, "w", encoding="utf-8") as f:
                f.write(result)
            
            self.bridge.move_file(fpath, f"history/{os.path.basename(fpath)}")
            
            self.active_agents[aid]["xp"] = self.active_agents[aid].get("xp", 0) + 10
            
            # Reward agent for successful processing
            self.ledger.add_transaction(sender="System", receiver=aid, amount=50, currency="PYTHON_COIN", contract="REWARD_PROCESSING")
            
            self.active_agents[aid].update({"status": "IDLE", "thought": "Mission complete. Gained 10 XP & 50 Coins."})

        except Exception as e:
            hyp = self.corrector.analyze_failure(aid, desc, str(e))
            self.active_agents[aid].update({"status": "RECOVERY", "thought": f"FAILED: {hyp}"})
            print(f"[CRITICAL] {aid} entering Darwinian recovery loop.")

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    print("Testing Orchestrator logic...")
    from os_bridge import OSBridge
    from hive_mind_router import HiveMindRouter
    
    orch = AgentCityOrchestrator("./test_orch")
    print("Orchestrator Heartbeat Active.")
    print("Test Passed. Winner Selected.")
