import os
import ctypes
import shutil

# PART 1: THE OS & HARDWARE METABOLISM
# Phase 2: The Action Protocols (Steps 101-200)
# ROAD BUILDER: Mapping network protocols to city transit.

class RoadBuilder:
    """
    Step 151-175: Transit Mapping
    FTP = ROADS (Bulk infrastructure, heavy lifting)
    TCP = WALKING (Steady, verified packets, human-scale reliability)
    UDP = BIKES (Fast, nimble, no overhead, occasional crashes)
    """
    def __init__(self, city_root):
        self.city_root = os.path.abspath(city_root)

    def build_road(self, source, alias_name):
        """Creates a Symlink (Road) to an external directory (FTP-style bulk link)."""
        target_path = os.path.join(self.city_root, alias_name)
        try:
            # Requires admin for true symlinks on Windows, or Developer Mode
            os.symlink(source, target_path, target_is_directory=True)
            return True, f"Road established to {source} via {alias_name}"
        except Exception as e:
            # Fallback to Directory Junction if possible
            return False, f"Road construction failed: {str(e)}"

    def protocol_dispatch(self, data_packet, mode="TCP"):
        """Dispatches data based on the Transit Metaphor."""
        if mode == "TCP":
            # 'Walking' - slow, verified
            return {"transit_type": "WALK", "reliability": "100%", "speed": "LOW"}
        elif mode == "UDP":
            # 'Bicycle' - fast, no verification
            return {"transit_type": "BIKE", "reliability": "BEST_EFFORT", "speed": "HIGH"}
        elif mode == "FTP":
            # 'Road' - infrastructure for bulk
            return {"transit_type": "ROAD", "reliability": "STABLE", "speed": "MEDIUM"}
        return {"transit_type": "UNKNOWN"}

    def bulldoze(self, path):
        """Step 101-150: Safe deletion (move to city trash)."""
        trash_dir = os.path.join(self.city_root, "city_trash")
        if not os.path.exists(trash_dir): os.makedirs(trash_dir)
        
        target = os.path.join(self.city_root, path)
        if os.path.exists(target):
            shutil.move(target, os.path.join(trash_dir, os.path.basename(path)))
            return True, f"Entity bulldozed to {trash_dir}"
        return False, "Target not found."

if __name__ == "__main__":
    # Step 8: Natural Selection Test
    builder = RoadBuilder("./test_road_city")
    if not os.path.exists("./test_road_city"): os.makedirs("./test_road_city")
    
    print("Testing Transit Protocols...")
    tcp_walk = builder.protocol_dispatch({}, "TCP")
    udp_bike = builder.protocol_dispatch({}, "UDP")
    
    print(f"TCP Protocol Mapping: {tcp_walk['transit_type']}")
    print(f"UDP Protocol Mapping: {udp_bike['transit_type']}")
    
    if tcp_walk['transit_type'] == "WALK" and udp_bike['transit_type'] == "BIKE":
        print("Test Passed. Winner Selected.")
