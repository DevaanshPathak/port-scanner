# Port Scanner

A basic port scanner built in python to learn about TCP connections, networking and the socket library in python.

Input host IP, start and end ports it will scan the range of ports and tell which is open.

It works by connecting to that port, then:
- If connection succeeds, port is open.
- If connection is refused, port is closed.
- If no response before timeout then port is filtered by a firewall.

To run, do `python main.py` in the repo's directory.