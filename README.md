# PyAlias

Fast, persistent command aliases for Windows that work exactly like native commands.

## Features

✓ **Native behavior** - Works in cmd.exe, PowerShell, Git Bash, any terminal  
✓ **Persistent** - Survives restarts and terminal sessions  
✓ **Speedy** - Written in C, launches in milliseconds
✓ **Auto-install** - Adds itself to PATH automatically  
✓ **Simple** - 200 lines of Python, 200 lines of C  

## Installation
```bash
pip install git+https://github.com/offerrall/PyAlias-Windows-Alias-Manager
```

**Requirements:** 
- Windows
- Python 3.10+
- gcc (MinGW-w64) - [Download here](https://www.mingw-w64.org/)

On first run, PyAlias automatically adds `~/.pyalias` to your PATH. Restart your terminal after installation.

## Quick Start
```bash
# Create aliases
pyalias new ls "dir /b"
pyalias new gs "git status"
pyalias new gp "git push"
pyalias new dev "cd C:\projects && npm run dev"

# Use them
ls
gs
gp origin main

# Manage
pyalias list
pyalias read ls
pyalias delete ls
```

## How It Works

**When you create an alias:**
1. PyAlias copies `launcher.exe` → `~/.pyalias/ls.exe`
2. Creates `~/.pyalias/ls.txt` containing the command

**When you run the alias:**
1. Windows finds `ls.exe` in PATH
2. `ls.exe` reads its own filename: "ls"
3. Opens `ls.txt` in the same directory
4. Executes the command with any arguments you passed
```
User types:    ls -la
Executes:      ls.exe → reads ls.txt ("dir /b") → runs "dir /b -la"
```

## Technical Details

**Launcher architecture:**
- Static memory allocation (no malloc)
- 32KB path buffer (handles Windows long paths)
- 8KB command buffer (practically unlimited)
- Error handling with specific messages

**Storage:**
- Aliases stored in `C:\Users\YourName\.pyalias\`
- Each alias is one `.exe` + one `.txt` file
- 50 aliases = ~1MB total

## Examples
```bash
# Git shortcuts
pyalias new gs "git status"
pyalias new ga "git add ."
pyalias new gc "git commit -m"
pyalias new gp "git push"

# Development
pyalias new dev "npm run dev"
pyalias new build "npm run build && npm test"

# System
pyalias new c "cls"
pyalias new e "exit"
```

## Limitations

These are inherent to how subprocesses work, not PyAlias limitations:

- **Can't change directory** - `cd` in a subprocess doesn't affect the parent shell
- **Can't modify environment** - `set VAR=value` only affects the subprocess

For these use cases, use shell-specific solutions (`.bashrc`, PowerShell profiles, etc.)

## Commands
```bash
pyalias new <alias> <command>    # Create alias
pyalias list                     # List all aliases  
pyalias read <alias>             # Show alias command
pyalias delete <alias>           # Delete alias
pyalias -h                       # Help
```

## License

MIT