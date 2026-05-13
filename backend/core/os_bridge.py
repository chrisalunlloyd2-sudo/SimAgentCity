import os
import shutil
import platform
import subprocess

class OSBridge:
    def __init__(self, root_dir):
        self.root_dir = os.path.abspath(root_dir)
        if not os.path.exists(self.root_dir):
            os.makedirs(self.root_dir, exist_ok=True)

    def move_file(self, source_rel_path, dest_rel_path):
        """Moves a file within the managed root directory."""
        source = os.path.normpath(os.path.join(self.root_dir, source_rel_path))
        dest = os.path.normpath(os.path.join(self.root_dir, dest_rel_path))
        
        if not os.path.exists(source):
            return False, f"Source {source} does not exist."
            
        try:
            # Ensure destination directory exists
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.move(source, dest)
            return True, f"Moved {source_rel_path} to {dest_rel_path}"
        except Exception as e:
            return False, str(e)

    def update_registry_mock(self, key, value):
        """Mock registry update for simulation (Real logic requires admin on Win)."""
        # This will be replaced with real winreg logic in the lock phase
        return True, f"Registry update simulation: {key} set to {value}"

    def get_file_tree(self):
        """Returns the current file topology for UI mapping."""
        tree = []
        for root, dirs, files in os.walk(self.root_dir):
            rel_root = os.path.relpath(root, self.root_dir)
            if rel_root == ".": rel_root = ""
            for name in files:
                tree.append({
                    "name": name,
                    "path": os.path.join(rel_root, name),
                    "type": "file"
                })
            for name in dirs:
                tree.append({
                    "name": name,
                    "path": os.path.join(rel_root, name),
                    "type": "folder"
                })
        return tree

if __name__ == "__main__":
    # Self-test logic for Step 8 (Natural Selection)
    test_dir = os.path.join(os.getcwd(), "test_city_tmp")
    if not os.path.exists(test_dir): os.makedirs(test_dir)
    with open(os.path.join(test_dir, "dummy.txt"), "w") as f: f.write("test")
    
    bridge = OSBridge(test_dir)
    success, msg = bridge.move_file("dummy.txt", "processed/dummy.txt")
    print(f"Self-Test: {success}, {msg}")
    
    # Cleanup
    if success:
        print("Test Passed. Winner Selected.")
