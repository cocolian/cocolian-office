#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
git -C "$root" submodule update --init --filter=blob:none
python3 - "$root" <<'PYTHON'
import json, subprocess, sys
from pathlib import Path
root=Path(sys.argv[1])
for item in json.loads((root/'repos.json').read_text()):
    repo=root/'src'/item['name']
    def git(*args):
        return subprocess.check_output(['git','-C',str(repo),*args],text=True).strip()
    if 'upstream' not in git('remote').splitlines():
        git('remote','add','upstream',item['upstream'])
    git('remote','set-url','--push','upstream','DISABLED')
    git('config','pull.ff','only')
    git('config','fetch.prune','true')
    git('config','remote.pushDefault','origin')
    head=git('rev-parse','HEAD')
    if head != item['commit']:
        raise SystemExit(f"Unexpected commit in {repo}: {head}")
    # Keep an existing branch at the locked commit; do not move a divergent branch.
    exists=subprocess.run(['git','-C',str(repo),'show-ref','--verify','--quiet','refs/heads/'+item['branch']]).returncode==0
    if exists and git('rev-parse',item['branch'])!=head:
        raise SystemExit(f"Existing branch diverges: {repo} {item['branch']}")
    if exists: git('switch',item['branch'])
    else: git('switch','-c',item['branch'])
    git('branch','--set-upstream-to','origin/'+item['branch'])
    print(item['name'],head)
PYTHON
