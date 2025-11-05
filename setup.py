from setuptools import setup
from setuptools.command.build_py import build_py
import subprocess
import sys
from pathlib import Path


class BuildWithC(build_py):
    
    def run(self):
        if sys.platform != "win32":
            print("WARNING: PyAlias only works on Windows")
            super().run()
            return
        
        c_file = Path("pyalias/launcher.c")
        exe_file = Path("pyalias/launcher.exe")
        
        if exe_file.exists():
            print(f"{exe_file} already exists, skipping compilation")
            super().run()
            return
        
        print("Checking for gcc...")
        try:
            subprocess.run(
                ["gcc", "--version"],
                capture_output=True,
                text=True,
                check=True
            )
            print("Found gcc")
        except FileNotFoundError:
            print("ERROR: gcc not found in PATH")
            print("PyAlias requires gcc to compile the launcher")
            sys.exit(1)
        
        print(f"Compiling {c_file}...")
        try:
            subprocess.run(
                ["gcc", str(c_file), "-o", str(exe_file), "-s", "-O2"],
                check=True
            )
            print(f"Successfully compiled {exe_file}")
        except subprocess.CalledProcessError as e:
            print(f"Compilation failed: {e}")
            sys.exit(1)
        
        super().run()


setup(
    cmdclass={'build_py': BuildWithC}
)