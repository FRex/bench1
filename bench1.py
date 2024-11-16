#!/usr/bin/env python3
"""Script to run a command and show its time and max resident set size (RAM usage)."""
import subprocess
import tempfile
import sys
import os


def main():
    """The main function, for performance and to not run on import."""

    tmpname = tempfile.NamedTemporaryFile(delete=False).name
    # tmpname = f"/tmp/bench1-tmp-pid-{os.getpid()}.txt"

    print(tmpname)

    args = ["time", "-v", "-o", tmpname] + sys.argv[1:]
    retcode = subprocess.run(args, check=False).returncode

    with open(tmpname, encoding="UTF-8") as tmpf:
        for line in map(str.strip, tmpf):
            print(line)

        # TODO: print pretty max rss, time elapsed in seconds, and retcode

    if os.path.exists(tmpname):
        os.remove(tmpname)

    sys.exit(retcode)


if __name__ == "__main__":
    main()
