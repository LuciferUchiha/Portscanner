import socket
import sys
import argparse
import concurrent.futures
import pyfiglet
from tqdm import tqdm

host_IP = None


def resolve_args():
    argv = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("host", type=_host, help="Hostname or IP of host system to be scanned")
    parser.add_argument("-s", "--startPort", type=_port, default=0, help="Port number to start scan (0-65535)")
    parser.add_argument("-e", "--endPort", type=_port, default=65535, help="Port number to end scan (0-65535)")
    return vars(parser.parse_args(argv))


def _host(s):
    try:
        value = socket.gethostbyname(s)
    except socket.gaierror:
        raise argparse.ArgumentTypeError(f"Host '{s}' could not be resolved.")
    return value


def _port(s):
    try:
        value = int(s)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Expected integer got '{s}'")
    if 0 > value > 65535:
        raise argparse.ArgumentTypeError(f"Port number must be 0-65535, got {port}")
    return value


def scan_tcp(port):
    global host_IP
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result = 0
    try:
        answer = sock.connect_ex((host_IP, port))
        if answer == 0:
            result = port
        sock.close()
    except socket.error:
        print(f"Could not connect to host '{host_IP}'")
        sys.exit()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit()

    return result


def print_open_ports(results):
    results = list(filter(None, results))
    for open_port in results:
        print(f"Port {open_port} is OPEN")


def main():
    args = resolve_args()
    pyfiglet.print_figlet("PORTSCANNER", font="slant")
    global host_IP
    host_IP = args.get("host")
    ports = range(args.get("startPort"), args.get("endPort") + 1)
    print(f"Starting scan of {host_IP}...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(tqdm(executor.map(scan_tcp, ports), total=len(ports)))
    print(f"Finished scan of {host_IP}!")
    print_open_ports(results)


if __name__ == "__main__":
    main()
