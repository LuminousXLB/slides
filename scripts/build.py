#!/bin/env python3
import subprocess
import sys
from pathlib import Path

import frontmatter


BASE = "/slides"
DIST = "dist"


def set_download_link(path: Path, download: str):
    with open(path, "r") as f:
        post = frontmatter.load(f)

    post["download"] = download

    with open(path, "wb") as f:
        frontmatter.dump(post, f)


def exec(args):
    print("$", *args)
    return subprocess.run(args, check=True)


if __name__ == "__main__":
    for path in Path.cwd().glob("*.md"):
        if not path.is_file():
            sys.exit(f"{path}: File not found.")

        rel = path.absolute().relative_to(Path.cwd()).with_suffix("")
        dist = DIST / rel
        base = BASE / rel
        file_path = base.with_suffix(".pdf")
        file_dist = DIST / rel.with_suffix(".pdf")

        print("rel", rel, sep="\t")
        print("dist", dist, sep="\t")
        print("base", base, sep="\t")
        print("file_path", file_path, sep="\t")
        print("file_dist", file_dist, sep="\t")

        set_download_link(path, str(file_path))
        exec([str(x) for x in ["slidev", "build", path, "--out", dist, "--base", base]])
        exec([str(x) for x in ["slidev", "export", path, "--output", file_dist]])
