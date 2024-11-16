# bench1

A Python script that runs a command using time, and prints its elapsed real time,
peak RSS (from time command), and return code, and forwards the return code.

Requires GNU time, not BusyBox one. On Windows msys provides GNU time exe.

# examples

```
$ bench1 sleep 3
{
    "seconds": 3.0469,
    "exit_code": 0,
    "max_rss": "10.4 MiB"
}

$ bench1 false
{
    "seconds": 0.0356,
    "exit_code": 1,
    "max_rss": "10.1 MiB"
}

$ bench1 rg test | tail -n 5
{
    "seconds": 0.2032,
    "exit_code": 0,
    "max_rss": "5.3 MiB"
}
```
