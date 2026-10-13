"""Control work 1: Docker command demonstration, variant 8.
Version: 1.0. Author: Romeiko Matvey Dmitrievich. Date: 2026-10-13.
Purpose: Record real build, lifecycle, network, volume and Task 2A results.
"""

import json
from pathlib import Path
import shlex
import subprocess
import uuid


def main():
    """Create isolated demo resources, record commands and remove demo objects."""
    root = Path(__file__).resolve().parents[1]
    evidence = root/"evidence"/"docker"
    evidence.mkdir(parents=True, exist_ok=True)
    records = []
    suffix = uuid.uuid4().hex[:8]
    image = "kr1-variant8:" + suffix
    alias = "kr1-variant8:verified-" + suffix
    container, network, volume = ["kr1-v8-{}-{}".format(kind, suffix)
                                  for kind in ("container", "network", "volume")]

    def run(section, arguments, stdin=None):
        """Capture one actual command and abort if it fails."""
        process = subprocess.run(arguments, input=stdin, text=True,
                                 stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                 cwd=root, timeout=600)
        record = {"section": section, "command": shlex.join(arguments),
                  "output": process.stdout, "exit_code": process.returncode}
        records.append(record)
        (evidence/"commands.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
        print("$", record["command"], flush=True)
        print(process.stdout, end="", flush=True)
        if process.returncode:
            raise subprocess.CalledProcessError(process.returncode, arguments)
        return process.stdout

    run("versions", ["docker", "version"])
    run("build", ["docker", "build", "--progress=plain", "-f", "Task3/Dockerfile", "-t", image, "."])
    run("tag", ["docker", "tag", image, alias])
    run("images", ["docker", "images", "kr1-variant8"])
    run("2a-env", ["docker", "run", "--rm", "-e", "TEXT=Вариант 8, 2026", image])
    run("2a-stdin", ["docker", "run", "--rm", "-i", image], "abc12345\n")
    run("2a-argument", ["docker", "run", "--rm", image, "--text", "Задача 8: 0123456789"])
    run("network", ["docker", "network", "create", network])
    run("network", ["docker", "network", "ls", "--filter", "name="+network])
    run("volume", ["docker", "volume", "create", volume])
    run("volume", ["docker", "volume", "ls", "--filter", "name="+volume])
    try:
        run("2a-volume", ["docker", "run", "--rm", "-v", volume+":/data",
                           "--entrypoint", "python", image, "-c",
                           "from pathlib import Path; Path('/data/input.txt').write_text('Текст 800 и 15', encoding='utf-8')"])
        run("2a-volume", ["docker", "run", "--rm", "-v", volume+":/data", image,
                           "--file", "/data/input.txt", "--output", "/data/result.txt"])
        run("2a-volume", ["docker", "run", "--rm", "-v", volume+":/data",
                           "--entrypoint", "python", image, "-c",
                           "from pathlib import Path; print(Path('/data/result.txt').read_text(encoding='utf-8'), end='')"])
        run("volume", ["docker", "volume", "inspect", "--format", "{{.Name}} {{.Driver}}", volume])
        run("run", ["docker", "run", "-d", "--name", container, "--network", network,
                     "-v", volume+":/data", "--entrypoint", "python", image, "-u", "-c",
                     "import time; print('Variant 8 lifecycle demo', flush=True); time.sleep(300)"])
        run("ps", ["docker", "ps", "--filter", "name="+container])
        run("logs", ["docker", "logs", container])
        run("pause", ["docker", "pause", container])
        run("pause", ["docker", "inspect", "--format", "{{.State.Status}} paused={{.State.Paused}}", container])
        run("unpause", ["docker", "unpause", container])
        run("restart", ["docker", "restart", "-t", "1", container])
        run("stop", ["docker", "stop", "-t", "1", container])
        run("stop", ["docker", "ps", "-a", "--filter", "name="+container])
        run("start", ["docker", "start", container])
        run("inspect", ["docker", "inspect", "--format",
                        "name={{.Name}} image={{.Config.Image}} status={{.State.Status}} mounts={{json .Mounts}}", container])
        run("network", ["docker", "network", "inspect", "--format", "{{.Name}} driver={{.Driver}}", network])
    finally:
        run("cleanup", ["docker", "rm", "-f", container])
        run("cleanup", ["docker", "network", "rm", network])
        run("cleanup", ["docker", "volume", "rm", volume])
    run("cleanup", ["docker", "image", "rm", alias, image])


if __name__ == "__main__":
    main()
