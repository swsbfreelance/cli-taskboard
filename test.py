import subprocess
import sys

for i in range(1000):
    subprocess.run([
        sys.executable, "-m", "taskboard",
        "add", f"Stress test {i}", "--priority", "low"
    ])