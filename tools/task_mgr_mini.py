import psutil
import json

def get_process_summary():
    """AI-Compatible Task Manager: Returns lightweight process list for agent analysis."""
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            # Filter for high-impact or relevant processes to keep it lightweight
            if proc.info['cpu_percent'] > 0.1 or proc.info['memory_info'].rss > 100 * 1024 * 1024:
                processes.append({
                    "pid": proc.info['pid'],
                    "name": proc.info['name'],
                    "cpu": proc.info['cpu_percent'],
                    "mem_mb": round(proc.info['memory_info'].rss / (1024 * 1024), 2)
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return sorted(processes, key=lambda x: x['cpu'], reverse=True)[:10]

if __name__ == "__main__":
    print(json.dumps(get_process_summary(), indent=4))
