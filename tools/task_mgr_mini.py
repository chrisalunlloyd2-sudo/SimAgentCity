import psutil
import json
import os

# PART 1: THE OS & HARDWARE METABOLISM
# Phase 2: The Action Protocols (Steps 176-200)
# BI-DIRECTIONAL PROCESS HOOKS (The Sprite Task Manager)

def get_process_summary():
    """AI-Compatible Task Manager: Returns lightweight process list for agent analysis."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            # Filter for high-impact or relevant processes to keep it lightweight
            if proc.info['cpu_percent'] > 0.1 or proc.info['memory_info'].rss > 50 * 1024 * 1024:
                processes.append({
                    "pid": proc.info['pid'],
                    "name": proc.info['name'],
                    "cpu": proc.info['cpu_percent'],
                    "mem_mb": round(proc.info['memory_info'].rss / (1024 * 1024), 2),
                    "type": "process_building"
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return sorted(processes, key=lambda x: x['cpu'], reverse=True)[:20]

def kill_process(pid):
    """Step 176-200: Demolish a process sprite to kill the OS process."""
    try:
        proc = psutil.Process(pid)
        name = proc.name()
        proc.terminate() # Graceful exit
        return True, f"Process {name} (PID: {pid}) demolished."
    except psutil.NoSuchProcess:
        return False, "Process no longer exists (already demolished)."
    except psutil.AccessDenied:
        return False, "Access Denied: Process is protected by the OS."
    except Exception as e:
        return False, str(e)

if __name__ == "__main__":
    # Step 8: Natural Selection Test
    print("Testing Process Summary...")
    procs = get_process_summary()
    print(f"Found {len(procs)} active process buildings.")
    
    if len(procs) > 0:
        print("Test Passed. Winner Selected.")
    else:
        print("Test Failed: No processes detected.")
