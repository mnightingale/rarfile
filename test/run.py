import sys
import subprocess

py = sys.argv[1]
crypto = sys.argv[2] if len(sys.argv) > 2 else ""

print(f"Running tests: py={py}, crypto={crypto}")

subprocess.run([
    sys.executable,
    "-m",
    "pytest",
    "-n", "auto",
    "--cov=rarfile",
    "--cov-report=term",
    "--cov-report=html:cover/" + py + (f"-{crypto}" if crypto else ""),
], check=True)

subprocess.run([
    sys.executable,
    "-m",
    "test.run_dump",
    py,
    crypto,
], check=True)
