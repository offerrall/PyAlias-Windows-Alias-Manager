import winreg

def add_to_path(directory: str) -> bool:
    """Add directory to user PATH"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE)
        current_path, _ = winreg.QueryValueEx(key, "Path")
        
        if directory in current_path.split(";"):
            winreg.CloseKey(key)
            return False
        
        new_path = f"{directory};{current_path}"
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        winreg.CloseKey(key)
        return True
    except:
        return False

def remove_from_path(directory: str) -> bool:
    """Remove directory from user PATH"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ | winreg.KEY_WRITE)
        current_path, _ = winreg.QueryValueEx(key, "Path")
        
        paths = current_path.split(";")
        if directory not in paths:
            winreg.CloseKey(key)
            return False
        
        paths.remove(directory)
        new_path = ";".join(paths)
        winreg.SetValueEx(key, "Path", 0, winreg.REG_EXPAND_SZ, new_path)
        winreg.CloseKey(key)
        return True
    except:
        return False

def is_in_path(directory: str) -> bool:
    """Check if directory is in PATH"""
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Environment", 0, winreg.KEY_READ)
        current_path, _ = winreg.QueryValueEx(key, "Path")
        winreg.CloseKey(key)
        return directory in current_path.split(";")
    except:
        return False