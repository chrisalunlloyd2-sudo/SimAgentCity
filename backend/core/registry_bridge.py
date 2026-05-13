import winreg
import os

class RegistryBridge:
    def __init__(self):
        self.hives = {
            "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
            "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE
        }
        # Step 26-50: Define a safe zone for write operations
        self.safe_prefix = "Software\\SimAgentCity"

    def get_keys(self, hive_name, subkey=""):
        """Reads registry keys to visualize them as buildings."""
        if hive_name not in self.hives:
            return []
        
        keys = []
        try:
            with winreg.OpenKey(self.hives[hive_name], subkey) as key:
                i = 0
                while True:
                    try:
                        name = winreg.EnumKey(key, i)
                        keys.append({
                            "name": name,
                            "path": f"{hive_name}\\{subkey}\\{name}" if subkey else f"{hive_name}\\{name}",
                            "type": "registry_building"
                        })
                        i += 1
                    except OSError:
                        break
        except Exception as e:
            print(f"Registry Access Error: {e}")
            
        return keys

    def read_value(self, hive_name, subkey, value_name):
        """AI-Compatible function: Read a registry value for agent analysis."""
        try:
            with winreg.OpenKey(self.hives[hive_name], subkey) as key:
                value, regtype = winreg.QueryValueEx(key, value_name)
                return value
        except Exception as e:
            return str(e)

    def write_value(self, hive_name, subkey, value_name, value):
        """Step 26-50: Safe write-operation in HKCU namespace."""
        if hive_name != "HKEY_CURRENT_USER":
            return False, "Write access restricted to HKEY_CURRENT_USER for safety."
        
        # Enforce safe zone
        if not subkey.startswith(self.safe_prefix):
            return False, f"Write access restricted to {self.safe_prefix} namespace."

        try:
            # Ensure key exists
            key = winreg.CreateKey(self.hives[hive_name], subkey)
            winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, str(value))
            winreg.CloseKey(key)
            return True, f"Successfully updated {value_name} in {subkey}"
        except Exception as e:
            return False, str(e)

    def delete_value(self, hive_name, subkey, value_name):
        """Step 26-50: Bulldozer protocol (Part 1)."""
        if hive_name != "HKEY_CURRENT_USER" or not subkey.startswith(self.safe_prefix):
            return False, "Unauthorized deletion attempt outside safe zone."

        try:
            with winreg.OpenKey(self.hives[hive_name], subkey, 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, value_name)
                return True, f"Deleted {value_name} from {subkey}"
        except Exception as e:
            return False, str(e)

if __name__ == "__main__":
    # Step 8: Natural Selection Test
    rb = RegistryBridge()
    
    print("Testing Registry Write (Safe Zone)...")
    success, msg = rb.write_value("HKEY_CURRENT_USER", "Software\\SimAgentCity\\TestBuilding", "Status", "Functional")
    print(f"Write Test: {success}, {msg}")
    
    if success:
        val = rb.read_value("HKEY_CURRENT_USER", "Software\\SimAgentCity\\TestBuilding", "Status")
        print(f"Read Verification: {val}")
        
        # Cleanup (Bulldozer check)
        del_success, del_msg = rb.delete_value("HKEY_CURRENT_USER", "Software\\SimAgentCity\\TestBuilding", "Status")
        print(f"Delete Test: {del_success}, {del_msg}")
        
        if del_success:
            print("Test Passed. Winner Selected.")
    else:
        print(f"Test Failed: {msg}")
