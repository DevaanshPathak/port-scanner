import socket
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


def main() -> None:
    host = input("Target host: ").strip()

    if not host:
        print("A target host is required.")
        return

    try:
        start_port = int(input("Start port: "))
        end_port = int(input("End port: "))
    except ValueError:
        print("Ports must be numbers.")
        return

    if not 1 <= start_port <= 65535:
        print("Start port must be between 1 and 65535.")
        return

    if not 1 <= end_port <= 65535:
        print("End port must be between 1 and 65535.")
        return

    if start_port > end_port:
        print("Start port cannot be greater than end port.")
        return

    try:
        target_ip = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"Could not resolve host: {host}")
        return

    open_ports: list[int] = []

    total_ports = end_port - start_port + 1
    worker_count = min(100, total_ports)

    print(f"\nScanning {host} ({target_ip})")
    print(f"Ports {start_port}-{end_port}")
    print(f"Workers: {worker_count}\n")

    try:
        with ThreadPoolExecutor(max_workers=worker_count) as executor:
            future_to_port = {
                executor.submit(scan_port, target_ip, port): port
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