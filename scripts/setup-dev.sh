#!/usr/bin/env bash
set -euo pipefail
root="$(cd "$(dirname "$0")/.." && pwd)"
git -C "$root" submodule update --init --depth 1 --filter=blob:none
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
    ref='refs/remotes/origin/'+item['branch']
    if subprocess.run(['git','-C',str(repo),'show-ref','--verify','--quiet',ref]).returncode:
        git('fetch','--depth','1','origin',item['branch']+':'+ref)
    git('branch','--set-upstream-to','origin/'+item['branch'])
    if item.get('base_branch'):
        base_ref='refs/remotes/origin/'+item['base_branch']
        git('fetch','--depth','1','--filter=blob:none','origin',item['base_branch']+':'+base_ref)
        baseline=item['base_commit']
        # Pin the server's build baseline even if the remote main branch advances.
        if subprocess.run(['git','-C',str(repo),'cat-file','-e',baseline+'^{commit}']).returncode:
            git('fetch','--depth','1','--filter=blob:none','origin',baseline)
        for branch in ('main','feature/notebookbar-icon-tooltips','feature/zh-cn-toolbar'):
            if subprocess.run(['git','-C',str(repo),'show-ref','--verify','--quiet','refs/heads/'+branch]).returncode:
                git('branch',branch,baseline)
    print(item['name'],head)
PYTHON
