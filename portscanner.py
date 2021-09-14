import socket
import sys
import concurrent.futures
import pyfiglet


def tcp_scanner(host_IP, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    try:
        result = sock.connect_ex((host_IP, port))  # returns “0” if connection goes
        if result == 0:
            print(f"Port {port} is OPEN")
        sock.close()

    except socket.error:
        print(f"Could not connect to host {host_IP}")
        sys.exit()
    except KeyboardInterrupt:
        print("Exiting...")
        sys.exit()


def read_host_IP():
    host = input("Enter host to scan: ")
    try:
        host_IP = socket.gethostbyname(host)
    except socket.gaierror:
        print(f"Host {host} could not be resolved. Exiting...")
        sys.exit()

    return host_IP


if __name__ == "__main__":
    pyfiglet.print_figlet("PORTSCANNER", font="slant")
    print(sys.argv)
    host_IP = read_host_IP()
    print(f"Starting scan of {host_IP}...")

    with concurrent.futures.ThreadPoolExecutor() as executor:
        for port in range(65536):  # Hosts have 65535 ports
            executor.submit(tcp_scanner, host_IP, port)
    print(f"Finished scan of {host_IP}!")
