import winreg
import os

class RegistryBridge:
    def __init__(self):
        self.hives = {
            "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER,
            "HKEY_LOCAL_MACHINE": winreg.HKEY_LOCAL_MACHINE
        }

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

if __name__ == "__main__":
    # Self-test for Step 8 (Natural Selection)
    rb = RegistryBridge()
    keys = rb.get_keys("HKEY_CURRENT_USER", "Software")
    print(f"Found {len(keys)} registry buildings in HKCU\\Software")
    if len(keys) > 0:
        print("Test Passed. Winner Selected.")
