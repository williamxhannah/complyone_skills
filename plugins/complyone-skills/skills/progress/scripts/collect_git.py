#!/usr/bin/env python3
"""List commits since a date across every git repo under a root folder.

Usage: python3 collect_git.py --since YYYY-MM-DD [--root ~/apps] [--until YYYY-MM-DD]

Reads each repo's main branch (main, else master, else HEAD). Skips worktrees
(.git is a file there) and anything under .claude/worktrees. Read-only: runs
only `git log` / `git rev-parse`; never fetches, pulls or changes anything.
Prints JSON: {"since":..., "repos":[{"repo", "branch", "commits":[{"date","sha","subject"}]}]}
"""
import json
import subprocess
import sys
from pathlib import Path


def arg(name, default=None):
    a = sys.argv[1:]
    return a[a.index(name) + 1] if name in a else default


def git(repo, *args):
    r = subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def main():
    since = arg("--since")
    if not since:
        sys.stderr.write("collect_git: ERROR: --since YYYY-MM-DD is required\n")
        sys.exit(1)
    until = arg("--until")
    root = Path(arg("--root", "~/apps")).expanduser()
    if not root.is_dir():
        sys.stderr.write("collect_git: ERROR: no such folder %s\n" % root)
        sys.exit(1)
    out = []
    for repo in sorted(p for p in root.iterdir() if (p / ".git").is_dir()):
        branch = next((b for b in ("main", "master") if git(repo, "rev-parse", "--verify", "-q", b)), "HEAD")
        cmd = ["log", branch, "--since=%s 00:00" % since, "--date=short", "--pretty=%ad%x09%h%x09%s"]
        if until:
            cmd.append("--until=%s 23:59" % until)
        log = git(repo, *cmd)
        if not log:
            continue
        commits = []
        for line in log.splitlines():
            parts = line.split("\t", 2)
            if len(parts) == 3:
                commits.append({"date": parts[0], "sha": parts[1], "subject": parts[2]})
        out.append({"repo": repo.name, "branch": branch, "commits": commits})
    json.dump({"since": since, "until": until, "root": str(root), "repos": out}, sys.stdout, indent=1)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
