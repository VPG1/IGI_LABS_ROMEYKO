"""Control work 1: Git command demonstration, variant 8.
Version: 1.0. Author: Romeiko Matvey Dmitrievich. Date: 2026-10-13.
Purpose: Reproduce the folder structure and local Git tasks in a new checkout.
"""

import argparse
from datetime import datetime, timedelta
import json
from pathlib import Path
import shlex
import subprocess


def main():
    """Record real CLI commands and keep all modifications in the given checkout."""
    parser = argparse.ArgumentParser(description="Задание 1, вариант 8")
    parser.add_argument("--destination", type=Path, required=True)
    parser.add_argument("--repository", default="https://github.com/VPG1/IGI_LABS_ROMEYKO.git")
    parser.add_argument("--group", default="GROUP_NUMBER")
    parser.add_argument("--list-number", default="NUMBER_IN_LIST")
    args = parser.parse_args()
    root = args.destination.resolve()
    if root.exists():
        parser.error("Каталог назначения уже существует; выберите новый каталог.")
    package = Path(__file__).resolve().parents[1]
    evidence = package/"evidence"/"git"
    evidence.mkdir(parents=True, exist_ok=True)
    records=[]

    def run(section, command, cwd=None):
        """Execute a CLI command, preserve its output and require success."""
        cwd = cwd or root
        process = subprocess.run(command, shell=True, cwd=cwd, executable="/bin/bash",
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 text=True, timeout=120)
        record = {"section":section,"command":command,"output":process.stdout,
                  "exit_code":process.returncode}
        records.append(record)
        (evidence/"commands.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
        print("$",command,flush=True)
        print(process.stdout,end="",flush=True)
        if process.returncode:
            raise subprocess.CalledProcessError(process.returncode,command)
        return process.stdout.strip()

    def status(section):
        """Show tracked, staged and untracked file state around a mutation."""
        run(section,"git status --short")

    def mutate(section,command):
        """Record before/after state for a file or index mutation."""
        status(section)
        output=run(section,command)
        status(section)
        return output

    root.parent.mkdir(parents=True,exist_ok=True)
    run("1","git --version",root.parent)
    run("1","git clone {} {}".format(shlex.quote(args.repository),shlex.quote(str(root))),root.parent)
    run("1","git config user.name 'Ромейко Матвей Дмитриевич'")
    run("1","git config user.email 'student@example.invalid'")
    run("1","git config core.quotepath false")
    run("1","git config --local --list")
    folders=["IGI","IGI/KR1","IGI/IPR1","STRWEB","STRWEB/KR1","STRWEB/IPR1",
             "IGI/KR1/bin","IGI/KR1/bin/700","IGI/KR1/bin/700/which","IGI/KR1/bin/700/which/700",
             "IGI/KR1/foo","IGI/KR1/foo/441","IGI/KR1/foo/441/bar","IGI/KR1/foo/441/bar/664",
             "IGI/KR1/foo/441/example","IGI/KR1/foo/441/example/200",
             "IGI/KR1/foo/441/baz","IGI/KR1/foo/441/baz/244"]
    run("2","mkdir -p "+" ".join(shlex.quote(folder) for folder in folders))
    for folder in folders:
        run("2","printf '%s\\n' {} > {}".format(
            shlex.quote("Test file for "+folder),shlex.quote(folder+"/"+Path(folder).name+"Test.txt")))
    run("2","printf '%s\\n' 'Repository root test' > {}".format(
        shlex.quote(root.name+"Test.txt")))
    run("2","printf '%s\\n' '000' > IGI/KR1/foo/441/test.txt")
    run("2","printf '%s\\n' '411' > IGI/KR1/foo/441/baz/244/readme.txt")
    run("2","find IGI STRWEB -type f | sort")
    run("2","cat IGI/KR1/foo/441/test.txt IGI/KR1/foo/441/baz/244/readme.txt")
    run("3","git clone https://github.com/smartiqaorg/geometric_lib.git IGI/KR1/geometric_lib")
    run("3","git submodule add https://github.com/smartiqaorg/geometric_lib.git IGI/KR1/geometric_lib")
    run("3","git submodule status")
    mutate("4a","git add IGI STRWEB .gitmodules "+shlex.quote(root.name+"Test.txt"))
    mutate("4b","printf '%s\\n' 'Edited after staging' >> IGI/IGITest.txt")
    run("4b","git diff -- IGI/IGITest.txt")
    run("4b","git diff --cached --stat")
    mutate("4c","git commit -m 'Create variant 8 folder structure and submodule'")
    mutate("4c","git add IGI/IGITest.txt")
    mutate("4c","git commit -m 'Edit IGI test file'")
    mutate("4d","printf '%s\\n' 'single temporary file' > single.tmp")
    mutate("4d","printf '%s\\n' 'first' > first.tmp; printf '%s\\n' 'second' > second.tmp")
    mutate("4d","git add '*.tmp'")
    mutate("4d","git commit -m 'Add single file and temporary file group'")
    mutate("4d","git rm single.tmp")
    mutate("4d","git rm -- '*.tmp'")
    mutate("4d","git commit -m 'Remove single file and temporary file group'")
    mutate("4e","git mv STRWEB/STRWEBTest.txt STRWEB/STRWEBRenamedTest.txt")
    mutate("4e","git commit -m 'Rename STRWEB test file'")
    mutate("4e","git mv STRWEB/STRWEBRenamedTest.txt STRWEB/STRWEBTest.txt")
    mutate("4e","git commit -m 'Restore required folder test filename'")
    run("4f","git submodule deinit -f IGI/KR1/geometric_lib")
    branches={"IGI":["STRWEB"],"STRWEB":["IGI"],
              "IGI-KR1":["STRWEB","IGI/IPR1"],"IGI-IPR1":["STRWEB","IGI/KR1"],
              "STRWEB-KR1":["IGI","STRWEB/IPR1"],"STRWEB-IPR1":["IGI","STRWEB/KR1"]}
    for branch,excluded in branches.items():
        run("4f","git switch main")
        run("4f","git switch -c "+branch)
        mutate("4f","git rm -r -- "+" ".join(excluded))
        mutate("4f","git commit -m "+shlex.quote("Keep folders for branch "+branch))
        run("4f","git ls-tree -r --name-only HEAD")
    run("4f","git switch main")
    run("4f","git submodule update --init")
    run("4f","git branch --list")
    today=datetime.now().date()
    before=(today-timedelta(days=1)).isoformat()
    after=(today+timedelta(days=1)).isoformat()
    for flags in ["--oneline --all","-n 3 --oneline",
                  "--since="+before+" --oneline", "--after="+before+" --oneline",
                  "--until="+after+" --oneline", "--before="+after+" --oneline",
                  "--author='Ромейко' --oneline","--committer='Ромейко' --oneline",
                  "--grep='Rename' --oneline"]:
        run("4g","git log "+flags)
    for flags in ["-p -n 1","--stat -n 2","--shortstat -n 2","--name-only -n 2",
                  "--name-status -n 2","--relative-date -n 2",
                  "--pretty=format:'%h %an %s' -n 3","--graph --oneline --all"]:
        run("4h","git log "+flags)
    run("4i","git log --all --format='%H' | while read commit; do git show --format=short --stat --patch \"$commit\"; done")
    mutate("4j","printf '%s\\n' '8' > test.txt")
    mutate("4j","git add test.txt")
    mutate("4j","git commit -m 'Add variant number 8'")
    mutate("4j","git revert --no-edit HEAD")
    run("4j","git log -n 2 --oneline")
    mutate("4k","printf '%s\\n' 'Unstage demonstration' >> IGI/IGITest.txt")
    mutate("4k","git add IGI/IGITest.txt")
    mutate("4k","git restore --staged IGI/IGITest.txt")
    run("4l","git diff -- IGI/IGITest.txt")
    mutate("4l","git restore IGI/IGITest.txt")
    run("4l","git diff --exit-code")
    run("5a","git remote -v")
    run("5b","git remote show origin")
    run("5b","git fetch origin")
    run("5d","git remote rename origin coursework")
    run("5d","git remote -v")
    run("5d","git remote rename coursework origin")
    (evidence/"repository.json").write_text(json.dumps({"root":str(root),
        "group":args.group,"list_number":args.list_number,"variant":8,
        "repository":args.repository},ensure_ascii=False,indent=2),encoding="utf-8")


if __name__ == "__main__":
    main()
