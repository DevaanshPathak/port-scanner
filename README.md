# Port Scanner

A basic port scanner built in python to learn about TCP connections, networking and the socket library in python.

Input host IP, start and end ports it will scan the range of ports and tell which is open.

It works by connecting to that port, then:
- If connection succeeds, port is open.
- If connection is refused, port is closed.
- If no response before timeout then port is filtered by a firewall.

Also added a counter which shows the number of ports scanned/total number of ports to be scanned.
Looks something like this:
```
Scanned 17/65535 ports
```

Added hyperthreading using ThreadPoolExecutor for faster scanning.

To run, do `python main.py` in the repo's directory.