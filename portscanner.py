import socket
import sys
import argparse
import concurrent.futures
import pyfiglet
from tqdm import tqdm

ports = []
host_IP = ""


def resolve_args():
    argv = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("host", type=host, help="Hostname or IP of host system to be scanned")
    parser.add_argument("-s", "--startPort", type=port, default=0, help="Port number to start scan (0-65535)")
    parser.add_argument("-e", "--endPort", type=port, default=65535, help="Port number to end scan (0-65535)")
    return vars(parser.parse_args(argv))


def host(s):
    try:
        host_IP = socket.gethostbyname(s)
    except socket.gaierror:
        raise argparse.ArgumentTypeError(f"Host '{s}' could not be resolved.")
    return host_IP


def port(s):
    try:
        port = int(s)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Expected integer got '{s}'")
    if port > 65535 or port < 0:
        raise argparse.ArgumentTypeError(f"Port number must be 0-65535, got {port}")
    return port


def scan_tcp(port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    try:
        result = sock.connect_ex((host_IP, port))
        if result == 0:
            # print(f"Port {port} is OPEN")
            return port
        sock.close()

    except socket.error:
        print(f"Could not connect to host '{host_IP}'")
        sys.exit()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit()


def print_open_ports(results):
    results = list(filter(None, results))
    for open_port in results:
        print(f"Port {open_port} is OPEN")


def main():
    args = resolve_args()
    pyfiglet.print_figlet("PORTSCANNER", font="slant")
    host_IP = args.get("host")
    ports = range(args.get("startPort"), args.get("endPort") + 1)
    print(f"Starting scan of {host_IP}...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(scan_tcp, ports), total=len(ports)))
    print(f"Finished scan of {host_IP}!")
    print_open_ports(results)


if __name__ == "__main__":
    main()
