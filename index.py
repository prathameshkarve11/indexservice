import socket
import threading
from queue import Queue
import time

# Queue to hold ports
port_queue = Queue()

# List to store open ports
open_ports = []

# Lock for thread-safe operations
lock = threading.Lock()

def scan_port(target, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((target, port))
        
        if result == 0:
            with lock:
                open_ports.append(port)
                print(f"[+] Port {port} is OPEN")
        
        sock.close()
    except Exception as e:
        pass


def worker(target):
    while not port_queue.empty():
        port = port_queue.get()
        scan_port(target, port)
        port_queue.task_done()


def fill_queue(start_port, end_port):
    for port in range(start_port, end_port + 1):
        port_queue.put(port)


def start_scan(target, start_port, end_port, thread_count=50):
    print(f"\nScanning target: {target}")
    print(f"Port range: {start_port}-{end_port}")
    print(f"Threads: {thread_count}\n")

    start_time = time.time()

    fill_queue(start_port, end_port)

    threads = []
    for _ in range(thread_count):
        t = threading.Thread(target=worker, args=(target,))
        t.start()
        threads.append(t)

    port_queue.join()

    end_time = time.time()

    print("\nScan Completed!")
    print(f"Time taken: {round(end_time - start_time, 2)} seconds")
    print(f"Open ports: {sorted(open_ports)}")


def resolve_target(target):
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        print("Error: Unable to resolve hostname.")
        return None


def main():
    print("=== Python Port Scanner ===")

    target = input("Enter target (IP or domain): ")
    start_port = int(input("Start port: "))
    end_port = int(input("End port: "))

    ip = resolve_target(target)

    if ip:
        start_scan(ip, start_port, end_port)


if __name__ == "__main__":
    main()