import sys
import os
import argparse
import json

# Add backend to path to reuse the core logic
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))
from core.agent_registrar import AgentRegistrar

def main():
    parser = argparse.ArgumentParser(description="SimAgentCity Registrar Tool")
    parser.add_argument("--register", action="store_true", help="Register a new agent")
    parser.add_argument("--name", help="Agent name")
    parser.add_argument("--role", help="Agent role (Miner, Processor, Shipper)")
    parser.add_argument("--list", action="store_true", help="List registered agents")
    
    args = parser.parse_args()
    
    registrar = AgentRegistrar(os.path.join(os.getcwd(), "agents_population.json"))
    
    if args.register:
        if not args.name or not args.role:
            print("Error: Name and Role required for registration.")
            return
        agent = registrar.register_agent(args.name, args.role)
        print(f"Agent {agent['name']} ({agent['id']}) successfully registered in the population.")
        
    if args.list:
        agents = registrar.get_registered_agents()
        print(json.dumps(agents, indent=4))

if __name__ == "__main__":
    main()
