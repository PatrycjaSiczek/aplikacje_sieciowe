import sys
import socket

if len(sys.argv) != 2:
    sys.exit(1)

host = sys.argv[1]

try:
    ip = socket.gethostbyname(host)
except socket.gaierror:
    print("Niepoprawny adres.")
    sys.exit(1)

print("Skanowanie\n")

for port in range(1, 1025):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    try:
        result = s.connect_ex((ip, port))
        if result == 0:
            try:
                sock = socket.getservbyport(port, 'tcp')
            except(socket.error, OverflowError):
                sock = "nieznana"

            print(f"Port {port} jest otwarty, usluga = {sock}")

    except socket.error:
        pass
    finally:
        s.close()

print("\nSkanowanie zakończone")

# Wyniki:
# python zadanie8.py google.com
# Skanowanie
# Port 80 jest otwarty, usluga = http
# Port 443 jest otwarty, usluga = https
# Skanowanie zakończone
