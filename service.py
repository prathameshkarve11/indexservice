import socket

# Common port → service mapping
COMMON_SERVICES = {
    20: "FTP (Data)",
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    67: "DHCP",
    68: "DHCP",
    69: "TFTP",
    80: "HTTP",
    110: "POP3",
    119: "NNTP",
    123: "NTP",
    137: "NetBIOS",
    138: "NetBIOS",
    139: "NetBIOS",
    143: "IMAP",
    161: "SNMP",
    179: "BGP",
    443: "HTTPS",
    445: "SMB",
    465: "SMTPS",
    500: "ISAKMP",
    587: "SMTP (Submission)",
    636: "LDAPS",
    989: "FTPS",
    990: "FTPS",
    993: "IMAPS",
    995: "POP3S",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt"
}


def grab_banner(ip, port):
    try:
        sock = socket.socket()
        sock.settimeout(1)
        sock.connect((ip, port))

        try:
            banner = sock.recv(1024).decode().strip()
            return banner
        except:
            return "No banner"

    except:
        return None
    finally:
        sock.close()


def detect_service(port):
    return COMMON_SERVICES.get(port, "Unknown Service")


def analyze_ports(ip, open_ports):
    print("\n=== Service Detection ===\n")

    for port in open_ports:
        service = detect_service(port)
        banner = grab_banner(ip, port)

        print(f"Port {port}")
        print(f"  Service : {service}")
        print(f"  Banner  : {banner}")
        print("-" * 30)


if __name__ == "__main__":
    print("Run this file from main scanner (import it).")