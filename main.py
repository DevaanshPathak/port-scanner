import socket
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed

def scan_port(host: str, port: int, timeout: float = 0.5) -> bool:
    """Return True when a TCP connection to the port succeeds."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return result == 0

    except OSError as error:
        print(f"\nNetwork error while scanning port {port}: {error}")
        return False

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scan a target for open TCP ports."
    )
    parser.add_argument(
        "host",
        help="Hostname or IPv4 address to scan.",
    )
    parser.add_argument(
        "-s",
        "--start-port",
        type=int,
        default=1,
        help="First port to scan (default: 1).",
    )
    parser.add_argument(
        "-e",
        "--end-port",
        type=int,
        default=65535,
        help="Last port to scan (default: 65535).",
    )
    parser.add_argument(
        "-w",
        "--workers",
        type=int,
        default=100,
        help="Max number of workers (default: 100).",
    )
    parser.add_argument(
        "-t",
        "--timeout",
        type=float,
        default=0.5,
        help="Timeout in seconds for each port scan (default: 0.5).",
    )

    return parser.parse_args()


def main() -> None:
    
    args = parse_arguments()

    host = args.host
    start_port = args.start_port
    end_port = args.end_port
    workers = args.workers
    timeout = args.timeout

    if not 1 <= start_port <= 65535:
        print("Start port must be between 1 and 65535.")
        return

    if not 1 <= end_port <= 65535:
        print("End port must be between 1 and 65535.")
        return

    if start_port > end_port:
        print("Start port cannot be greater than end port.")
        return
    
    if workers < 1:
        print("Number of workers must be at least 1.")
        return
    
    if timeout <= 0:
        print("Timeout must be a positive number.")
        return
    
    if workers > 500:
        print("Worker count may not exceed 500.")

    try:
        target_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"Could not resolve host: {host}")
        return

    open_ports: list[int] = []

    total_ports = end_port - start_port + 1
    worker_count = min(workers, total_ports)

    print(f"\nScanning {host} ({target_ip})")
    print(f"Ports {start_port}-{end_port}")
    print(f"Workers: {worker_count}\n")

    try:
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            future_to_port = {
                executor.submit(scan_port, target_ip, port, timeout): port
                for port in range(start_port, end_port + 1)
            }

            for scanned_count, future in enumerate(
                as_completed(future_to_port),
                start=1,
            ):
                port = future_to_port[future]

                try:
                    is_open = future.result()
                except Exception as error:
                    print(f"\nError scanning port {port}: {error}")
                    continue

                print(
                    f"\rScanned {scanned_count}/{total_ports} ports",
                    end = "",
                    flush = True,
                )

                if is_open:
                    open_ports.append(port)

                    try:
                        service = socket.getservbyport(port)
                    except OSError:
                        service = "Unknown"

                    print(f"\n[OPEN] {port}/tcp - {service}")

    except KeyboardInterrupt:
        print("\nScan cancelled.")
        return

    print("\n\nScan complete.")

    if open_ports:
        print(f"Open ports: {', '.join(map(str, open_ports))}")
    else:
        print("No open ports found.")


if __name__ == "__main__":
    main()