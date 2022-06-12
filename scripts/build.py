#!/bin/env python3
from glob import glob
import subprocess
import sys
from pathlib import Path


BASE = "/slides"

for path in Path.cwd().glob("*.md"):

    if not path.is_file():
        sys.exit(f"{path}: File not found.")

    rel = path.absolute().relative_to(Path.cwd()).with_suffix("")
    dist = "dist" / rel
    base = BASE / rel

    args = [str(x) for x in ["slidev", "build", path, "--out", dist, "--base", base, "--download"]]
    print("$", *args)
    subprocess.run(args, check=True)
