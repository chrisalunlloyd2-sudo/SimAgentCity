import json
import os

# PART 2: THE 1995 SIM-UI FRAMEWORK
# Phase 6: Dynamic Districts & Zoning (Steps 501-550)
# ZONING MANAGER: Persists functional state of grid tiles.

class ZoningManager:
    def __init__(self, storage_path):
        self.storage_path = storage_path
        self.zones = {} # (x, y): zone_type
        self.load_zones()

    def set_zone(self, x, y, zone_type):
        """Step 501-550: Map-specific functional zoning."""
        self.zones[f"{x},{y}"] = zone_type
        self.save_zones()

    def get_zone(self, x, y):
        return self.zones.get(f"{x},{y}", "RESIDENTIAL")

    def save_zones(self):
        with open(self.storage_path, "w") as f:
            json.dump(self.zones, f, indent=4)

    def load_zones(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    self.zones = json.load(f)
            except:
                self.zones = {}

    def get_all_zones(self):
        """Returns zones for UI rendering."""
        return self.zones

if __name__ == "__main__":
    # Step 8: Natural Selection Test
    print("Testing Zoning Manager...")
    zm = ZoningManager("./test_zones.json")
    zm.set_zone(5, 5, "INDUSTRIAL")
    zone = zm.get_zone(5, 5)
    print(f"Zone at 5,5: {zone}")
    
    if zone == "INDUSTRIAL":
        print("Test Passed. Winner Selected.")
    
    # Cleanup
    if os.path.exists("./test_zones.json"):
        os.remove("./test_zones.json")
