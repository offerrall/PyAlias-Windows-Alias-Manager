# PyAlias

Fast, persistent command aliases for Windows that work exactly like native commands.

## Features

✓ **Native behavior** - Works in cmd.exe, PowerShell, Git Bash, any terminal  
✓ **Persistent** - Survives restarts and terminal sessions  
✓ **Fast** - 21x faster than .bat files (0.75ms vs 15ms per execution)  
✓ **Reliable** - Works correctly with arguments in automation scripts  
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

## Commands
```bash
pyalias new <alias> <command>    # Create alias
pyalias list                     # List all aliases  
pyalias read <alias>             # Show alias command
pyalias delete <alias>           # Delete alias
pyalias -h                       # Help
```

## Why Not Just Use .bat Files?

You might wonder: "Windows already supports `.bat` files, why do I need this?"

**.bat files have critical limitations:**

1. **20x slower** - Batch files take ~15ms to execute vs ~0.75ms for `.exe`
2. **Arguments break in automation** - `.bat` files don't pass arguments correctly when called from Python's `subprocess`
   - Your automation scripts will fail
   - `.exe` works reliably everywhere

3. **Batch syntax quirks** - Need `@echo off`, special escaping for `%`, `&`, `|`
   - `.exe` just runs the command directly

**Benchmark from real tests:**
```
100 executions in cmd.exe:
  .exe:  75ms   (0.75ms each)
  .bat:  1579ms (15.79ms each)
  
Result: .exe is 21x faster
```

## How It Works

**When you create an alias:**
1. PyAlias copies `launcher.exe` → `~/.pyalias/ls.exe`
2. Creates `~/.pyalias/ls.txt` containing the command
3. Adds `~/.pyalias` to your PATH (once)

**When you run the alias:**
1. Windows finds `ls.exe` in PATH
2. `ls.exe` reads its own filename: "ls"
3. Opens `ls.txt` in the same directory
4. Executes the command with any arguments you passed
```
User types:    ls -la
Executes:      ls.exe → reads ls.txt ("dir /b") → runs "dir /b -la"
```

## Why C?

The launcher is written in C for speed and reliability:

- **Instant execution** - No interpreter overhead like batch files
- **Static memory** - No malloc, deterministic behavior
- **Robust** - Handles long paths (32KB), large commands (8KB)
- **Portable** - Single 20KB executable per alias

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

## Limitations

These are inherent to how subprocesses work, not PyAlias limitations:

- **Can't change directory** - `cd` in a subprocess doesn't affect the parent shell
- **Can't modify environment** - `set VAR=value` only affects the subprocess

For these use cases, use shell-specific solutions (`.bashrc`, PowerShell profiles, etc.)

## Contributing

Pull requests welcome. Keep it simple and fast.

## License

MIT
