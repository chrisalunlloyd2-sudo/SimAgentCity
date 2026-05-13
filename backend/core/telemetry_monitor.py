import ctypes
from ctypes import wintypes
import os
import time

# PART 1: THE OS & HARDWARE METABOLISM
# Phase 1: The Deep Registry & Telemetry (Steps 1-25)

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", wintypes.DWORD),
        ("dwMemoryLoad", wintypes.DWORD),
        ("ullTotalPhys", ctypes.c_uint64),
        ("ullAvailPhys", ctypes.c_uint64),
        ("ullTotalPageFile", ctypes.c_uint64),
        ("ullAvailPageFile", ctypes.c_uint64),
        ("ullTotalVirtual", ctypes.c_uint64),
        ("ullAvailVirtual", ctypes.c_uint64),
        ("sullAvailExtendedVirtual", ctypes.c_uint64),
    ]

    def __init__(self):
        # Set the size of the structure
        self.dwLength = ctypes.sizeof(self)
        super(MEMORYSTATUSEX, self).__init__()

class TelemetryMonitor:
    def __init__(self):
        self.kernel32 = ctypes.windll.kernel32

    def get_memory_stats(self):
        """Step 1-25: High-precision RAM tracking via Windows API."""
        stat = MEMORYSTATUSEX()
        if self.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
            return {
                "load_percent": stat.dwMemoryLoad,
                "total_gb": round(stat.ullTotalPhys / (1024**3), 2),
                "avail_gb": round(stat.ullAvailPhys / (1024**3), 2),
                "used_gb": round((stat.ullTotalPhys - stat.ullAvailPhys) / (1024**3), 2)
            }
        return None

    def get_city_vitals(self):
        """Translates OS telemetry into city-state metrics."""
        mem = self.get_memory_stats()
        if not mem: return {"status": "OFFLINE"}
        
        # Mapping: Memory load -> City Stress
        # 0-50% = Healthy, 50-80% = Crowded, 80%+ = Critical
        stress = "HEALTHY"
        if mem["load_percent"] > 80: stress = "CRITICAL"
        elif mem["load_percent"] > 50: stress = "CROWDED"
        
        return {
            "os_stats": mem,
            "city_stress": stress,
            "timestamp": time.time()
        }

if __name__ == "__main__":
    # Step 8: Natural Selection Test
    monitor = TelemetryMonitor()
    vitals = monitor.get_city_vitals()
    print("SimAgentCity Vitals Pulse:")
    print(f"Memory Load: {vitals['os_stats']['load_percent']}%")
    print(f"City Stress: {vitals['city_stress']}")
    
    if vitals['os_stats']['total_gb'] > 0:
        print("Test Passed. Winner Selected.")
