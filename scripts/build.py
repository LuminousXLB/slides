#!/bin/env python3
import subprocess
import sys
from pathlib import Path

import frontmatter

WEBSITE = "https://www.shenjm.dev/slides/slide-01/1"
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
    with open("static/CNAME", "r") as f:
        CNAME = f.read().strip()

    for path in Path.cwd().glob("*.md"):
        if not path.is_file():
            sys.exit(f"{path}: File not found.")

        rel = path.absolute().relative_to(Path.cwd()).with_suffix("")
        html_dist = DIST / rel
        file_dist = DIST / rel.with_suffix(".pdf")

        html_base = BASE / rel
        file_path = f'https://{CNAME}{html_base.with_suffix(".pdf")}'

        print("rel", rel, sep="\t")
        print("html_dist", html_dist, sep="\t")
        print("html_base", html_base, sep="\t")
        print("file_path", file_path, sep="\t")
        print("file_dist", file_dist, sep="\t")

        set_download_link(path, str(file_path))
        exec([str(x) for x in ["slidev", "build", path, "--out", html_dist, "--base", html_base]])
        exec([str(x) for x in ["slidev", "export", path, "--output", file_dist]])
