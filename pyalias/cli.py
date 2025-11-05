import sys
from pathlib import Path
from shutil import copy
from pyalias.path_utils import add_to_path, is_in_path

ALIAS_DIR: Path = Path.home() / ".pyalias"
LAUNCHER_EXE: Path = Path(__file__).parent / "launcher.exe"

def auto_install() -> None:
    """Automatically install if not in PATH"""
    alias_dir_str = str(ALIAS_DIR)
    
    if not is_in_path(alias_dir_str):
        print(f"Installing PyAlias...")
        if add_to_path(alias_dir_str):
            print(f"Added to PATH: {alias_dir_str}")
            print("Restart your terminal for changes to take effect\n")
        else:
            print("WARNING: Could not add to PATH automatically\n")

def show_help() -> None:
    """Show help message"""
    help_text = """
PyAlias - Native command aliases for Windows

Usage: pyalias <command> [args]

Commands:
  new <alias> <cmd>    Create new alias
  list                 List all aliases
  delete <alias>       Delete alias
  read <alias>         Show alias command
  -h, --help           Show this help

Examples:
  pyalias new ls "dir /b"
  pyalias new gs "git status"
  pyalias list
  pyalias delete ls
"""
    print(help_text.strip())

def main() -> None:
    ALIAS_DIR.mkdir(exist_ok=True)
    auto_install()
    
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help"]:
        show_help()
        return
    
    command = sys.argv[1]
    
    if command == "new":
        if len(sys.argv) < 4:
            print("Usage: pyalias new <alias> <command>")
            return
        alias = sys.argv[2]
        command_str = " ".join(sys.argv[3:])
        cmd_new(alias, command_str)
    elif command == "list":
        cmd_list()
    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: pyalias delete <alias>")
            return
        alias = sys.argv[2]
        cmd_delete(alias)
    elif command == "read":
        if len(sys.argv) < 3:
            print("Usage: pyalias read <alias>")
            return
        alias = sys.argv[2]
        cmd_read(alias)
    else:
        print(f"Unknown command: {command}")
        print("Use 'pyalias -h' for help")

def cmd_new(alias: str, command: str) -> None:
    """Create new alias"""
    alias_exe = ALIAS_DIR / f"{alias}.exe"
    alias_txt = ALIAS_DIR / f"{alias}.txt"
    
    if not LAUNCHER_EXE.exists():
        print(f"ERROR: launcher.exe not found at {LAUNCHER_EXE}")
        return
    
    copy(LAUNCHER_EXE, alias_exe)
    alias_txt.write_text(command.strip())
    
    print(f"Created: {alias} -> {command}")

def cmd_list() -> None:
    """List all aliases"""
    aliases = sorted([f.stem for f in ALIAS_DIR.glob("*.exe")])
    
    if not aliases:
        print("No aliases found")
        return
    
    print(f"Total aliases: {len(aliases)}")
    for alias in aliases:
        txt_file = ALIAS_DIR / f"{alias}.txt"
        if txt_file.exists():
            command = txt_file.read_text().strip()
            print(f"  {alias} -> {command}")
        else:
            print(f"  {alias} -> (no command file)")

def cmd_delete(alias: str) -> None:
    """Delete alias"""
    alias_exe = ALIAS_DIR / f"{alias}.exe"
    alias_txt = ALIAS_DIR / f"{alias}.txt"
    
    deleted = False
    
    if alias_exe.exists():
        alias_exe.unlink()
        deleted = True
    
    if alias_txt.exists():
        alias_txt.unlink()
        deleted = True
    
    if deleted:
        print(f"Deleted: {alias}")
    else:
        print(f"Alias not found: {alias}")

def cmd_read(alias: str) -> None:
    """Read alias command"""
    alias_txt = ALIAS_DIR / f"{alias}.txt"
    
    if not alias_txt.exists():
        print(f"Alias not found: {alias}")
        return
    
    command = alias_txt.read_text().strip()
    print(f"{alias} -> {command}")

if __name__ == "__main__":
    main()