import socket
import sys
import argparse
import concurrent.futures
import pyfiglet


def scan_tcp(host_IP, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    try:
        result = sock.connect_ex((host_IP, port))  # returns “0” if connection goes
        if result == 0:
            print(f"Port {port} is OPEN")
        sock.close()

    except socket.error:
        print(f"Could not connect to host '{host_IP}'")
        sys.exit()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit()


def host(host):
    try:
        host_IP = socket.gethostbyname(host)
    except socket.gaierror:
        raise argparse.ArgumentTypeError(f"Host '{host}' could not be resolved.")
    return host_IP


def resolve_args():
    argv = sys.argv[1:]
    parser = argparse.ArgumentParser()
    parser.add_argument("host", type=host, help="Hostname or IP of host system to be scanned")

    return vars(parser.parse_args(argv))


def main():
    args = resolve_args()
    pyfiglet.print_figlet("PORTSCANNER", font="slant")
    host_IP = args.get("host")
    print(f"Starting scan of {host_IP}...")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for port in range(65536):  # Hosts have 65535 ports
            executor.submit(scan_tcp, host_IP, port)
    print(f"Finished scan of {host_IP}!")


if __name__ == "__main__":
    main()
