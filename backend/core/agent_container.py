import os
import shutil
import json

# PART 1: THE OS & HARDWARE METABOLISM
# Phase 3: Agent Spawning & Local Sandboxing (Steps 201-300)
# AGENT CONTAINER: Localized sandboxing for recruited Sims.

class AgentContainerManager:
    def __init__(self, workspace_root):
        self.agents_root = os.path.join(workspace_root, "agents")
        if not os.path.exists(self.agents_root):
            os.makedirs(self.agents_root)

    def spawn_agent_home(self, agent_id):
        """Steps 201-250: Creates an isolated physical environment for a Sim."""
        agent_dir = os.path.join(self.agents_root, agent_id)
        subdirs = ["home", "inventory", "logs", "temp"]
        
        try:
            if not os.path.exists(agent_dir):
                os.makedirs(agent_dir)
                for sd in subdirs:
                    os.makedirs(os.path.join(agent_dir, sd))
            
            return True, f"Agent {agent_id} environment spawned at {agent_dir}"
        except Exception as e:
            return False, str(e)

    def mount_volume(self, agent_id, source_path, target_alias):
        """Steps 251-300: Maps a physical folder into the agent's inventory."""
        agent_inventory = os.path.join(self.agents_root, agent_id, "inventory")
        target_link = os.path.join(agent_inventory, target_alias)
        
        try:
            # Create a symbolic link (volume mount)
            # Note: requires developer mode or admin on Windows
            if os.path.exists(target_link):
                return True, "Volume already mounted."
                
            os.symlink(source_path, target_link, target_is_directory=os.path.isdir(source_path))
            return True, f"Volume {source_path} mounted to agent {agent_id}/{target_alias}"
        except Exception as e:
            # Fallback: Copy content if symlink fails (Mining simulation)
            return False, f"Volume mount failed: {str(e)}"

    def get_agent_storage_stats(self, agent_id):
        """AI-Compatible: Check disk usage of a specific agent's sandbox."""
        agent_dir = os.path.join(self.agents_root, agent_id)
        total_size = 0
        if os.path.exists(agent_dir):
            for dirpath, dirnames, filenames in os.walk(agent_dir):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    total_size += os.path.getsize(fp)
        return {"id": agent_id, "disk_usage_kb": round(total_size / 1024, 2)}

if __name__ == "__main__":
    # Step 8: Natural Selection Test
    print("Testing Agent Sandboxing...")
    manager = AgentContainerManager("./test_city_root")
    
    success, msg = manager.spawn_agent_home("test_sim_1")
    print(f"Spawn Test: {success}, {msg}")
    
    if success:
        # Step 251-300 check
        stats = manager.get_agent_storage_stats("test_sim_1")
        print(f"Sandbox Stats: {stats}")
        
        print("Test Passed. Winner Selected.")
    
    # Cleanup
    if os.path.exists("./test_city_root"):
        shutil.rmtree("./test_city_root")
