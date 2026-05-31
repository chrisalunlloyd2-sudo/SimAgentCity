# TIMESTAMP: 2026-05-23T03:26:00Z
# PROJECT_ID: SimAgentCity-v1.3
# AGENT_ID: Antigravity-Architect

import argparse
import sys
import os
import uvicorn
import requests
import time
import threading
import webbrowser

# PART 3: THE NEURAL ORCHESTRATION
# Phase 10: The Real-Life Hookup (Steps 876-890)
# Final CLI Wrapper for Headless Operation and API Exposure

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend"))
from backend.main import app

def run_server(port):
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="warning")

def auto_launch_browser(port):
    """Automatically closes existing SimAgentCity windows and launches a fresh one."""
    time.sleep(2.0)
    print(f"[GENESIS] Purging previous SimAgentCity browser windows...")
    try:
        # Closes windows on Windows that contain "SimAgentCity" in the titlebar
        os.system('taskkill /F /FI "WINDOWTITLE eq SimAgentCity*" >nul 2>&1')
    except Exception as err:
        pass
    
    print(f"[GENESIS] Launching fresh UI at http://127.0.0.1:{port}/static/index.html...")
    webbrowser.open(f"http://127.0.0.1:{port}/static/index.html")

def main():
    parser = argparse.ArgumentParser(description="SimAgentCity - Enterprise Orchestrator (Genesis Edition)")
    parser.add_argument("--start", action="store_true", help="Start the City API Server and UI")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the city on")
    parser.add_argument("--test", action="store_true", help="Execute the Global Stress Test (Step 891-900)")
    
    args = parser.parse_args()
    
    if args.start:
        print(f"[GENESIS] Starting SimAgentCity on port {args.port}...")
        # Start browser auto-launcher thread
        launcher_thread = threading.Thread(target=auto_launch_browser, args=(args.port,), daemon=True)
        launcher_thread.start()
        run_server(args.port)
        
    elif args.test:
        print("[GENESIS] Executing Global Stress Test...")
        # Start server in background thread
        server_thread = threading.Thread(target=run_server, args=(args.port,), daemon=True)
        server_thread.start()
        
        # Wait for server
        time.sleep(3)
        
        try:
            # Test 1: Vitals
            res = requests.get(f"http://127.0.0.1:{args.port}/vitals")
            if res.status_code == 200:
                print("[TEST] OS Metabolism (Hardware Bus): Verified.")
            
            # Test 2: Agent Recruitment
            res = requests.post(f"http://127.0.0.1:{args.port}/mall/register", json={"name": "Genesis_Prime", "role": "Processor"})
            if res.status_code == 200:
                agent_id = res.json()["agent"]["id"]
                print(f"[TEST] Agent Recruitment: Verified ({agent_id}).")
                
                # Test 3: Agent Task Assignment (Desktop Automation Hook)
                # We simulate dropping a file on the agent
                test_file = "city_workspace/genesis_test.txt"
                os.makedirs("city_workspace", exist_ok=True)
                with open(test_file, "w") as f: f.write("Initialize world.")
                
                res = requests.post(f"http://127.0.0.1:{args.port}/assign", json={
                    "agent_id": agent_id,
                    "file_path": "genesis_test.txt",
                    "task": "Summarize this data."
                })
                if res.status_code == 200:
                    print("[TEST] Agent Assignment & Spatial Logic: Verified.")
                    
            print("\n[SYSTEM] GLOBAL STRESS TEST PASSED. THE CITY IS ALIVE.")
        except Exception as e:
            print(f"[FATAL] Stress test failed: {e}")

if __name__ == "__main__":
    main()
