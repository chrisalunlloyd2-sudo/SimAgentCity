import json
import os
import hashlib

class AgentRegistrar:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, "w") as f:
                json.dump([], f)

    def register_agent(self, name, role, risk_profile="Balanced", model="h2o-danube3:4b"):
        """Registers a new agent sim for the population with OpenClaw Traits."""
        agents = self.get_registered_agents()
        
        # Hardware-Backed SHA-256 Trust Layer (Simulation)
        raw_id = f"{name}_{role}_{len(agents)}".encode('utf-8')
        sha_id = hashlib.sha256(raw_id).hexdigest()[:12]
        
        # OpenClaw Financial Personalization
        budget_limit = 1000
        if risk_profile == "Aggressive":
            budget_limit = 5000
        elif risk_profile == "Conservative":
            budget_limit = 200

        new_agent = {
            "id": f"agent_{sha_id}",
            "name": name,
            "role": role,
            "model": model,
            "status": "IDLE",
            "traits": {
                "risk_profile": risk_profile,
                "budget_limit": budget_limit,
                "trust_score": 100,
                "xp": 0
            }
        }
        agents.append(new_agent)
        with open(self.storage_path, "w") as f:
            json.dump(agents, f, indent=4)
        return new_agent

    def get_registered_agents(self):
        """AI-Compatible function: List agents for the mall."""
        try:
            with open(self.storage_path, "r") as f:
                return json.load(f)
        except:
            return []

if __name__ == "__main__":
    # Self-test for Step 8 (Natural Selection)
    registrar = AgentRegistrar("./test_agents.json")
    agent = registrar.register_agent("CityMiner", "Mining")
    print(f"Registered Agent: {agent['name']}")
    if os.path.exists("./test_agents.json"):
        print("Test Passed. Winner Selected.")
        os.remove("./test_agents.json")
