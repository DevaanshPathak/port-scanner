import socket
import sys

def scan_port(host: str, port:int, timeout: float=0.5) -> bool:
    # Return True when a TCP connection to the port succeeds.
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            return result == 0
    except socket.gaierror:
        print("Could not resolve host: ", host)
        sys.exit(1)
    except OSError as error:
        print("Network error while scanning port ", port,": ", error)
        return False
    
def main() -> None:
    host = input("Target host: ".strip())

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
        print("Could not resolve host: ", host)
        return
    
    print("Scanning ", host, " ", target_ip)
    print("Ports ", start_port, "-", end_port)

    open_ports: list[int] = []

    try:
        for port in range(start_port, end_port + 1):
            if scan_port(target_ip, port):
                open_ports.append(port)

                try:
                    service = socket.getservbyport(port, "tcp")
                except OSError:
                    service = "Unknown"

                print("[OPEN] ", [port],"/tcp - ", service)


    except KeyboardInterrupt:
        print("Scan cancelled.")
        return
    
    print("Scan complete.")

    if open_ports:
        print("Open ports: ", open_ports)
    else:
        print("No open ports found.")

if __name__ == "__main__":
    main()