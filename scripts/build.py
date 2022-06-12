#!/bin/env python3
import subprocess
import sys
from pathlib import Path

DIST = "dist"
BASE = "/slides"


def exec(args):
    print("$", *args, file=sys.stderr)
    return subprocess.run(args, check=True)


if __name__ == "__main__":
    with open("static/CNAME", "r") as f:
        CNAME = f.read().strip()

    for path in Path.cwd().glob("*.md"):
        if not path.is_file():
            sys.exit(f"{path}: File not found.")

        rel = path.absolute().relative_to(Path.cwd()).with_suffix("")
        dist = DIST / rel
        base = BASE / rel

        exec([str(x) for x in ["slidev", "build", path, "--out", dist, "--base", base, "--download"]])
