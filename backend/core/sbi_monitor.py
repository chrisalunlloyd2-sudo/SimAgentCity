import time
import json
import os

# PART 4: THE DECENTRALIZED FOUNDRY
# Phase 11: The Web3 Trap & DePIN (Steps 1001-1050)
# SBI MONITOR: Systemic Behavioral Interpolation (The City Interpol).

class SBIMonitor:
    def __init__(self, history_path):
        self.history_path = history_path
        self.behavior_trends = {} # agent_id: [spatial_coords]
        self.quarantine_zone = []

    def log_movement(self, agent_id, x, y):
        """Steps 1001-1025: Track agent travel patterns."""
        if agent_id not in self.behavior_trends:
            self.behavior_trends[agent_id] = []
        
        self.behavior_trends[agent_id].append({
            "x": x, "y": y, "t": time.time()
        })
        
        # Keep history manageable
        if len(self.behavior_trends[agent_id]) > 100:
            self.behavior_trends[agent_id].pop(0)

    def interpolate_behavior(self, agent_id):
        """Steps 1026-1050: Interpolation logic to detect anomalies."""
        history = self.behavior_trends.get(agent_id, [])
        if len(history) < 10:
            return "NORMAL (InSufficient Data)"
            
        # Analysis: Did the agent jump across the map instantly? (Logic leak/spoof)
        # Simplified: Check distance between last two points
        p1 = history[-2]
        p2 = history[-1]
        dist = abs(p1["x"] - p2["x"]) + abs(p1["y"] - p2["y"])
        
        if dist > 20: # Impossible city movement
            self.quarantine_zone.append(agent_id)
            return "ANOMALOUS (QUARANTINED)"
            
        return "NORMAL"

    def get_interpol_status(self):
        return {
            "monitored_population": len(self.behavior_trends),
            "quarantined_agents": self.quarantine_zone,
            "status": "ACTIVE"
        }

if __name__ == "__main__":
    # Step 8: Natural Selection Test
    print("Testing SBI Monitor (City Interpol)...")
    sbi = SBIMonitor("./test_sbi.json")
    
    # Simulate normal movement (11 points)
    for i in range(11):
        sbi.log_movement("Agent_A", i, i)
        
    # Simulate Logic Leak (Teleportation)
    sbi.log_movement("Agent_A", 50, 50)
    
    status = sbi.interpolate_behavior("Agent_A")
    print(f"Agent_A Behavior: {status}")
    
    if "QUARANTINED" in status:
        print("Test Passed. Winner Selected.")
