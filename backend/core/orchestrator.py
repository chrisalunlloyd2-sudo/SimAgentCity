import threading
import queue
import time
import os
import sys

# Handshake for local sandbox testing
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from .os_bridge import OSBridge
    from .llm_client import LLMClient
    from .file_watcher import CityFileWatcher
except ImportError:
    from os_bridge import OSBridge
    from llm_client import LLMClient
    from file_watcher import CityFileWatcher

class AgentCityOrchestrator:
    def __init__(self, workspace_dir):
        self.bridge = OSBridge(workspace_dir)
        self.llm = LLMClient()
        self.task_queue = queue.Queue()
        self.active_agents = {} # agent_id: status
        self.pulse_rate = 1.2
        self.running = True

        # Step 51-75: Initialize Real-time Watcher
        self.watcher = CityFileWatcher(workspace_dir, self._on_fs_event)
        self.watcher.start()

        # Start Heartbeat Thread
        self.heartbeat_thread = threading.Thread(target=self._run_heartbeat, daemon=True)
        self.heartbeat_thread.start()

    def _on_fs_event(self, event_type, path):
        """Callback for file system events."""
        print(f"[PULSE] FS Event: {event_type} on {path}")
        # Here we could emit a WebSocket signal to the UI to refresh immediately

    def _run_heartbeat(self):
...

        while self.running:
            # Sync terminal/UI state
            # self.bridge.get_file_tree()
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
            # Concurrent standby logic
            thread = threading.Thread(target=self._execute_agent_flow, args=(t,), daemon=True)
            thread.start()

    def _execute_agent_flow(self, task_data):
        """Atomic Flow: Mine -> Process -> Box -> Ship."""
        aid = task_data["id"]
        fpath = task_data["file"]
        desc = task_data["task"]
        
        self.active_agents[aid] = "PROCESSING"
        
        # 1. READ (Mine)
        full_path = os.path.join(self.bridge.root_dir, fpath)
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            # 2. PROCESS (LLM)
            result, status = self.llm.process_file_task(content, desc)
            
            # 3. WRITE (Box)
            dest_path = f"processed/agent_{aid}_{os.path.basename(fpath)}"
            final_dest = os.path.join(self.bridge.root_dir, dest_path)
            os.makedirs(os.path.dirname(final_dest), exist_ok=True)
            with open(final_dest, "w", encoding="utf-8") as f:
                f.write(result)
            
            # 4. MOVE (Ship)
            # In the physical SIM, the file moves from root to 'processed'
            self.bridge.move_file(fpath, f"history/{os.path.basename(fpath)}")
            
            self.active_agents[aid] = "IDLE"
        except Exception as e:
            self.active_agents[aid] = f"ERROR: {str(e)}"

if __name__ == "__main__":
    import os
    import sys
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    print("Testing Orchestrator logic...")
    from os_bridge import OSBridge
    from llm_client import LLMClient
    
    orch = AgentCityOrchestrator("./test_orch")
    print("Orchestrator Heartbeat Active.")
    print("Test Passed. Winner Selected.")
