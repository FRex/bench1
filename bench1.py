#!/usr/bin/env python3
"""Script to run a command and show its time and max resident set size (RAM usage)."""
from subprocess import run, PIPE
import json
import sys
import os
import humanize


def adjust_file(fname: str) -> int:
    with open(fname, encoding="UTF-8") as f:
        lines = f.read().splitlines()

    badtext = "Command exited with non-zero status"
    goodlines = [l for l in lines if not l.startswith(badtext)]
    badlines = [l for l in lines if l.startswith(badtext)]
    if not badlines:
        return 0  # nothing to do

    # write out adjusted lines and return the non-zero status code found
    with open(fname, "w", encoding="UTF-8") as f:
        for line in goodlines:
            print(line, file=f)

    return int(badlines[0].replace(badtext, "").strip())


def main():
    """main script function, wrapped for performance and to not run on import"""
    tmpname = f"/tmp/bench1-tmp-pid-{os.getpid()}.txt"
    if os.path.exists(tmpname):
        os.remove(tmpname)

    args = ["time", "-v", "-o", tmpname] + sys.argv[1:]
    retcode = run(args, check=False).returncode
    sub_command_status = adjust_file(tmpname)
    with open(tmpname, encoding="UTF-8") as tmpf:
        runret = run(["jc", "--time"], stdout=PIPE, stdin=tmpf, check=False)
    try:
        output = json.loads(runret.stdout)
        maxrss = output["maximum_resident_set_size"]
        seconds = output["elapsed_time_total_seconds"]
        humanrss = humanize.naturalsize(maxrss * 1024, True, format="%.3f")
        prettyout = {
            "maximum_resident_set_size": humanrss,
            "elapsed_time_total_seconds": f"{round(seconds, 4)} s",
            "return_code": sub_command_status,
        }
        print(json.dumps(prettyout, indent=4), file=sys.stderr)
        # print(f"{x}\n{elapsed_time_total_seconds} s\n", file=sys.stderr)
    except Exception as ex:  # pylint: disable=broad-except
        print(ex, file=sys.stderr)
        print(runret.stdout, file=sys.stderr)

    if os.path.exists(tmpname):
        os.remove(tmpname)

    sys.exit(retcode)


if __name__ == "__main__":
    main()
