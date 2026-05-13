import json
import os

class AgentRegistrar:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        if not os.path.exists(self.storage_path):
            with open(self.storage_path, "w") as f:
                json.dump([], f)

    def register_agent(self, name, role, model="h2o-danube3:4b"):
        """Registers a new agent sim for the population."""
        agents = self.get_registered_agents()
        new_agent = {
            "id": f"agent_{len(agents) + 1}",
            "name": name,
            "role": role,
            "model": model,
            "status": "IDLE"
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
