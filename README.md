# Python Port Scanner

A simple multithreaded TCP port scanner built in Python.

The scanner checks a target host for open TCP ports using Python sockets and `ThreadPoolExecutor`. It supports configurable port ranges, worker threads, connection timeouts, service-name lookup, and a live scan counter.

## Features

* Scan a hostname or IPv4 address
* Scan a configurable TCP port range
* Multithreaded scanning using `ThreadPoolExecutor`
* Live scan progress counter
* Configurable worker count
* Configurable connection timeout
* Automatic hostname resolution
* Common service-name lookup
* Sorted open-port results
* Command-line interface using `argparse`
* Graceful cancellation with `Ctrl+C`

## Requirements

* Python 3.9 or newer
* No external packages required

The project only uses modules from Python’s standard library:

* `argparse`
* `socket`
* `concurrent.futures`

## Installation

Clone the repository:

```bash
git clone https://github.com/devaanshpathak/port-scanner.git
cd port-scanner
```

No dependencies need to be installed.

## Usage

Run the scanner with:

```bash
python main.py HOST
```

Example:

```bash
python main.py localhost
```

By default, the scanner checks ports `1` through `1024` with `100` worker threads and a timeout of `0.5` seconds.

## Command-Line Options

```text
usage: main.py [-h] [-s START_PORT] [-e END_PORT]
               [-w WORKERS] [-t TIMEOUT] host
```

### Positional argument

| Argument | Description                      |
| -------- | -------------------------------- |
| `host`   | Hostname or IPv4 address to scan |

### Optional arguments

| Option               | Description                      | Default |
| -------------------- | -------------------------------- | ------- |
| `-h`, `--help`       | Display the help message         | —       |
| `-s`, `--start-port` | First port to scan               | `1`     |
| `-e`, `--end-port`   | Last port to scan                | `1024`  |
| `-w`, `--workers`    | Maximum number of worker threads | `100`   |
| `-t`, `--timeout`    | Connection timeout in seconds    | `0.5`   |

## Examples

### Scan the default port range

```bash
python main.py localhost
```

### Scan a custom port range

```bash
python main.py localhost -s 1 -e 10000
```

### Scan a specific port

```bash
python main.py localhost -s 8000 -e 8000
```

### Change the number of worker threads

```bash
python main.py localhost -s 1 -e 5000 -w 50
```

### Change the connection timeout

```bash
python main.py localhost -s 1 -e 10000 -t 0.2
```

### Use full argument names

```bash
python main.py localhost \
  --start-port 1 \
  --end-port 10000 \
  --workers 100 \
  --timeout 0.5
```

For PowerShell, the command can be written on one line:

```powershell
python main.py localhost --start-port 1 --end-port 10000 --workers 100 --timeout 0.5
```

### Show help

```bash
python main.py --help
```

## Example Output

```text
Scanning localhost (127.0.0.1)
Ports: 1-10000
Workers: 100
Timeout: 0.5 seconds

[OPEN] 8000/tcp - Unknown
Scanned 10000/10000 ports

Scan complete.
Open ports: 8000
```

## Testing Locally

You can safely test the scanner against your own computer.

Start a temporary HTTP server:

```bash
python -m http.server 8000
```

Open another terminal and scan the port:

```bash
python main.py localhost -s 7995 -e 8005
```

The scanner should detect port `8000` as open.

Stop the HTTP server using:

```text
Ctrl+C
```

## How It Works

The scanner creates a TCP socket for each port and attempts to connect using:

```python
sock.connect_ex((host, port))
```

A result of `0` means the TCP connection succeeded, so the port is considered open.

The scanner uses `ThreadPoolExecutor` to check multiple ports concurrently. This makes scanning faster because network operations spend much of their time waiting for responses.

Each submitted scan returns a `Future` object. The scanner uses `as_completed()` to process results as soon as individual scans finish.

Because threaded scans may finish out of order, the final list of open ports is sorted before being displayed.

## Service Detection

The scanner uses:

```python
socket.getservbyport(port, "tcp")
```

to display the conventional service associated with a port.

For example:

```text
22/tcp  - ssh
80/tcp  - http
443/tcp - https
```

This does not confirm which application is actually running on the port. A program can run on any available port, regardless of its conventional service assignment.

## Project Structure

```text
python-port-scanner/
├── main.py
└── README.md
```

## Current Limitations

* Supports TCP connect scanning only
* Supports IPv4 only
* Does not perform UDP scanning
* Does not detect operating systems
* Does not confirm actual service versions
* Does not distinguish reliably between closed and filtered ports
* Does not export results to files
* Submits all selected ports to the executor at the beginning of the scan

## Planned Improvements

* Flexible port input such as `22,80,443,8000-8100`
* Scan duration and ports-per-second statistics
* JSON and CSV exports
* Common-port scan presets
* Basic banner grabbing
* IPv6 support
* Improved port-state reporting
* Rich terminal progress bar and results table
* Configuration through command-line flags
* Unit tests

## Legal and Ethical Use

Only scan:

* Your own computer
* Your own servers
* Lab environments
* Systems for which you have explicit permission

Scanning systems without authorization may violate laws, policies, or terms of service.

This project is intended for education, development, and authorized security testing.

## License

This project is available under the MIT License.

## Author

Created by Devaansh Pathak as a Python networking and cybersecurity learning project.
