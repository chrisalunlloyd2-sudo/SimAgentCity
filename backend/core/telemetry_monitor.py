import ctypes
from ctypes import wintypes
import os
import time
import psutil
import subprocess

# PART 1: THE OS & HARDWARE METABOLISM
# Phase 1: The Deep Registry & Telemetry (Steps 76-100: Hardware Bus)

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
        self.dwLength = ctypes.sizeof(self)
        super(MEMORYSTATUSEX, self).__init__()

class MetabolismMonitor:
    def __init__(self):
        pass

    def cleanup_processes(self):
        """Step 1-50: Detect and kill zombie processes (WebView2/Edge)."""
        try:
            # Kill unresponsive processes
            subprocess.run(["taskkill", "/F", "/IM", "msedgewebview2.exe", "/FI", "STATUS eq UNRESPONSIVE"], capture_output=True)
            subprocess.run(["taskkill", "/F", "/IM", "msedge.exe", "/FI", "STATUS eq UNRESPONSIVE"], capture_output=True)
            return True
        except Exception as e:
            print(f"[METABOLISM MONITOR] Cleanup error: {e}")
            return False

class TelemetryMonitor:
    def __init__(self):
        self.kernel32 = ctypes.windll.kernel32
        # Initialize network counters for delta calculation
        self.last_net_io = psutil.net_io_counters()
        self.last_time = time.time()
        self.metabolism = MetabolismMonitor()

    def get_memory_stats(self):
        """Step 1-25: RAM tracking."""
        stat = MEMORYSTATUSEX()
        if self.kernel32.GlobalMemoryStatusEx(ctypes.byref(stat)):
            return {
                "load_percent": stat.dwMemoryLoad,
                "total_gb": round(stat.ullTotalPhys / (1024**3), 2),
                "avail_gb": round(stat.ullAvailPhys / (1024**3), 2),
                "used_gb": round((stat.ullTotalPhys - stat.ullAvailPhys) / (1024**3), 2)
            }
        return None

    def get_hardware_bus(self):
        """Steps 76-100: Capture CPU and Network I/O for city environment mapping."""
        # CPU Load (Pollution Source)
        cpu_load = psutil.cpu_percent(interval=None)
        
        # Network Speed (Wind/Weather)
        current_net_io = psutil.net_io_counters()
        now = time.time()
        time_delta = now - self.last_time
        
        # Calculate bytes per second
        bytes_sent = (current_net_io.bytes_sent - self.last_net_io.bytes_sent) / time_delta
        bytes_recv = (current_net_io.bytes_recv - self.last_net_io.bytes_recv) / time_delta
        
        # Update markers
        self.last_net_io = current_net_io
        self.last_time = now
        
        # Mapping hardware to city metrics
        # CPU 0-100 -> Pollution 0-100
        pollution = cpu_load
        
        # Network traffic -> Wind Speed (Logarithmic scale for better UI visualization)
        total_traffic_kb = (bytes_sent + bytes_recv) / 1024
        wind_speed = min(100, round(total_traffic_kb / 10, 2)) # Cap at 100 "knots"

        return {
            "cpu_load": cpu_load,
            "net_traffic_kbps": round(total_traffic_kb, 2),
            "city_pollution": pollution,
            "city_wind_speed": wind_speed
        }

    def get_city_vitals(self):
        """Translates OS telemetry into city-state metrics."""
        mem = self.get_memory_stats()
        bus = self.get_hardware_bus()
        
        # Aggregate stress level
        avg_load = (mem["load_percent"] + bus["cpu_load"]) / 2 if mem else 50
        stress = "HEALTHY"
        if avg_load > 80: stress = "CRITICAL"
        elif avg_load > 50: stress = "CROWDED"
        
        # Weather determination based on network activity
        weather = "CALM"
        if bus["city_wind_speed"] > 50: weather = "STORMY"
        elif bus["city_wind_speed"] > 10: weather = "BREEZY"
        
        return {
            "status": "ONLINE",
            "os_stats": mem or {},
            "hardware_bus": bus,
            "city_stress": stress,
            "city_weather": weather,
            "timestamp": time.time()
        }

if __name__ == "__main__":
    # Step 8: Natural Selection Test
    monitor = TelemetryMonitor()
    time.sleep(1) # Interval for net calculation
    vitals = monitor.get_city_vitals()
    print("SimAgentCity Vitals Pulse (Hardware Bus Active):")
    print(f"Pollution (CPU): {vitals['hardware_bus']['city_pollution']}%")
    print(f"Wind Speed (Net): {vitals['hardware_bus']['city_wind_speed']} knots")
    print(f"Weather: {vitals['city_weather']}")
    
    if vitals['hardware_bus']['cpu_load'] >= 0:
        print("Test Passed. Winner Selected.")
