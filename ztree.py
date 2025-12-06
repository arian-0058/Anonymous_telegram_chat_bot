#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from pathlib import Path
from fnmatch import fnmatch

DEFAULT_IGNORES = [
    ".git", ".venv", "venv", "env", "__pycache__", "node_modules",
    "dist", "build", ".mypy_cache", ".pytest_cache", ".idea", ".vscode"
]

BRANCH = "├── "
LAST   = "└── "
PIPE   = "│   "
SPACE  = "    "

def matches_any(name: str, patterns: list[str]) -> bool:
    return any(fnmatch(name, pat) for pat in patterns)

def list_children(path: Path, ignores: list[str], include_files: bool) -> tuple[list[Path], list[Path]]:
    dirs = []
    files = []
    for p in path.iterdir():
        if matches_any(p.name, ignores):
            continue
        if p.is_dir():
            dirs.append(p)
        elif include_files and p.is_file():
            files.append(p)
    dirs.sort(key=lambda x: x.name.lower())
    files.sort(key=lambda x: x.name.lower())
    return dirs, files

def build_lines(root: Path, ignores: list[str], max_depth: int | None, include_files: bool) -> list[str]:
    lines = [f"{root.resolve().name}"]
    def walk(dir_path: Path, prefix: str, depth: int):
        if max_depth is not None and depth >= max_depth:
            return
        dirs, files = list_children(dir_path, ignores, include_files)
        items = dirs + files
        for i, p in enumerate(items):
            connector = LAST if i == len(items) - 1 else BRANCH
            lines.append(prefix + connector + p.name)
            if p.is_dir():
                new_prefix = prefix + (SPACE if i == len(items) - 1 else PIPE)
                walk(p, new_prefix, depth + 1)
    walk(root, "", 0)
    return lines

def main():
    ap = argparse.ArgumentParser(
        description="Generate a directory tree and save it to a text file."
    )
    ap.add_argument("root", nargs="?", default=".", help="Root directory (default: current directory).")
    ap.add_argument("-o", "--output", default="tree.txt", help="Output file path (default: tree.txt).")
    ap.add_argument("-I", "--ignore", action="append", default=[],
                    help="Glob/pattern to ignore (can be used multiple times). Example: -I node_modules -I '*.pyc'")
    ap.add_argument("--no-files", action="store_true", help="List only directories (omit files).")
    ap.add_argument("-d", "--depth", type=int, default=None, help="Max depth (default: unlimited).")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Path not found or not a directory: {root}")

    ignores = list(DEFAULT_IGNORES) + args.ignore
    include_files = not args.no_files

    lines = build_lines(root, ignores, args.depth, include_files)

    out_path = Path(args.output).resolve()
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"✅ Tree saved to: {out_path}")

if __name__ == "__main__":
    main()
