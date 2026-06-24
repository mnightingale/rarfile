#!/usr/bin/env python3

import os
import sys
import subprocess
from difflib import unified_diff
from pathlib import Path

def normalize(lines):
    # Collapse runs of whitespace like diff -w.
    return [" ".join(line.split()) + "\n" for line in lines]

def main():
    if len(sys.argv) < 3:
        print(f"usage: {sys.argv[0]} PY TAG")
        return 1

    tag = sys.argv[2]

    os.environ["PYTHONIOENCODING"] = "utf8"
    # os.environ["PYTHONUTF8"] = "1"

    os.makedirs("tmp", exist_ok=True)

    diffs = f"tmp/output.{tag}.diffs"
    if os.path.exists(diffs):
        os.remove(diffs)

    quiet = True

    if quiet:
        print(f"[{tag}] testing structure dump")

    result = 0

    files = sorted(Path("test/files").glob("*.rar"))
    for f in map(Path.as_posix, files):
        if not quiet:
            print(f"{tag} -> {f:<30} .. ", end="", flush=True)

        output_file = f"{f}.{tag}"

        with open(output_file, "w", encoding="utf-8") as out:
            subprocess.run(
                [sys.executable, "dumprar.py", "-v", "-ppassword", f],
                stdout=out,
                env=os.environ,
                check=False,
            )

        with open(f"{f}.exp", encoding="utf-8") as a:
            expected = a.readlines()

        with open(output_file, encoding="utf-8") as b:
            actual = b.readlines()

        expected_norm = normalize(expected)
        actual_norm = normalize(actual)

        diff_lines = list(
            unified_diff(
                expected_norm,
                actual_norm,
                fromfile=f"{f}.exp",
                tofile=output_file,
                lineterm="",
            )
        )

        if not diff_lines:
            if not quiet:
                print("ok")
            os.remove(output_file)
        else:
            if not quiet:
                print("FAIL")

            errmsg = "FAILED"

            if f.endswith("-hpsw.rar"):
                errmsg = "failed-nocrypto"
            else:
                result = 1

            if quiet:
                print(f"[{tag}] {f:<30} .. {errmsg}")

            with open(diffs, "a", encoding="utf-8") as df:
                df.write(f"#### {sys.executable} ####\n")
                for line in diff_lines:
                    df.write(line)
                    if not line.endswith("\n"):
                        df.write("\n")

    if result != 0:
        print(f"Diffs: {diffs}")

    return result


if __name__ == "__main__":
    sys.exit(main())
