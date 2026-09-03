import subprocess
import sys
import os

current_dir = os.path.dirname(__file__)

subprocess.run([
    sys.executable,
    os.path.join(current_dir, "menu.py")
])