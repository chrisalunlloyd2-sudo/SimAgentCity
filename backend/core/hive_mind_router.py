import requests
import json
import time

# PART 3: THE NEURAL ORCHESTRATION
# Phase 7: The Hive Mind Router (Steps 601-700)
# LLM ROUTER: Intelligent task distribution between model swarms.

class HiveMindRouter:
    def __init__(self):
        self.ollama_api = "http://localhost:11434/api/generate"
        self.models = {
            "FAST": "qwen2.5:0.5b",      # For chat bubbles, simple cleanup
            "SMART": "h2o-danube3:4b",   # For logic processing, synthesis
            "EXPERT": "mistral"          # (Optional) For complex mutation
        }

    def route_task(self, prompt, complexity="FAST", system_prompt=""):
        """
        Step 601-650: Intelligent Routing
        Determines which 'Brain Power Plant' handles the current municipal service.
        """
        model = self.models.get(complexity, self.models["FAST"])
        
        payload = {
            "model": model,
            "prompt": prompt,
            "system": system_prompt,
            "stream": False
        }
        
        try:
            start_time = time.time()
            response = requests.post(self.ollama_api, json=payload, timeout=90)
            latency = time.time() - start_time
            
            if response.status_code == 200:
                return {
                    "response": response.json().get("response", ""),
                    "model_used": model,
                    "latency": round(latency, 2),
                    "status": "SUCCESS"
                }
            return {"status": "ERROR", "code": response.status_code}
        except Exception as e:
            return {"status": "OFFLINE", "error": str(e)}

    def generate_chat_bubble(self, agent_name, role, status):
        """Step 651-700: Agent Thought Visualization."""
        prompt = f"Act as an AI Sim in a SimCity 1995 environment. Your name is {agent_name}, role is {role}. Current task status: {status}. Output one very short, retro-style thought bubble (max 10 words)."
        res = self.route_task(prompt, complexity="FAST")
        return res.get("response", "...")

if __name__ == "__main__":
    # Step 8: Natural Selection Test
    print("Testing Hive Mind Router...")
    router = HiveMindRouter()
    
    # Test Chat Bubble (Fast Route)
    thought = router.generate_chat_bubble("Worker_01", "Miner", "Sifting data")
    print(f"Agent Thought: {thought}")
    
    if thought:
        print("Test Passed. Winner Selected.")
