import sys
import socket

if len(sys.argv) != 3:
    print("python zadanie.py <host> <port>")
    sys.exit(1)

host = sys.argv[1]
try:
    port = int(sys.argv[2])
except ValueError:
    print("Błąd w porcie - musi być liczbą")
    sys.exit(1)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    s.connect((host, port))

    try:
        usluga = socket.getservbyport(port, 'tcp')
    except:
        usluga = "blad"

    print(f"Port {port} otwarty na hoście {host}. - {usluga}")
    s.close()

except socket.timeout:
    print(f"Port {port} - timeout")
except Exception as e:
    print(f"Błąd")

# Wyniki:
# python zadanie7.py google.com 80
# Port 80 otwarty hoście google.com. - http

