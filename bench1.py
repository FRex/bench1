#!/usr/bin/env python3
"""Script to run a command and show its time and max resident set size (RAM usage)."""
import subprocess
import tempfile
import time
import json
import sys
import os


def prettysize(fsize: int) -> str:
    if fsize < 1024:
        return f"{fsize} Bytes"
    if fsize < 1024 * 1024:
        return f"{fsize / 1024:.1f} KiB"
    if fsize < 1024 * 1024 * 1024:
        return f"{fsize / (1024 * 1024):.1f} MiB"
    return f"{fsize / (1024 * 1024 * 1024):.1f} GiB"


def main():
    """The main function, for performance and to not run on import."""

    # create the temporary file safely and get its name
    tmpname = tempfile.NamedTemporaryFile(delete=False).name

    # run the command and get time and return code and save output over our temporary file
    args = ["time", "-v", "-o", tmpname] + sys.argv[1:]
    starttime = time.time()
    retcode = subprocess.run(args, check=False).returncode
    out = {"seconds": round(time.time() - starttime, 4), "exit_code": retcode}

    # get the RSS
    with open(tmpname, encoding="UTF-8") as tmpf:
        for line in map(str.strip, tmpf):
            need = "Maximum resident set size (kbytes):"
            if line.startswith(need):
                val = line.replace(need, "").strip()
                out["max_rss"] = prettysize(1024 * int(val))

    # make sure to remove the temporary file
    if os.path.exists(tmpname):
        os.remove(tmpname)

    # pretty print dict as json
    print(json.dumps(out, indent=4))

    # forward the exit code
    sys.exit(retcode)


if __name__ == "__main__":
    main()
