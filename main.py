#zadanie1

source = input("Nazwa pliku: ")
try:
    with open(source, "r", encoding="utf-8") as src:
        dest = src.read()
    with open("lab1zad1.txt", "w", encoding="utf-8") as dst:
        dst.write(dest)

except FileNotFoundError:
    print("Błąd - plik nie istnieje")


#Zadanie2

source = input("Nazwa pliku: ")

try:
    with open(source, "rb") as src:
        dest = src.read()
    with open("lab1zad1.png", "wb") as dst:
        dst.write(dest)

except FileNotFoundError:
    print("Błąd - plik nie istnieje")


#Zadanie3

import ipaddress

ip = input("Adres IP: ")

try:
    ipaddress.ip_address(ip)
    print("Adres IP poprawny.")
except ValueError:
    print("Adres IP niepoprawny.")

# Wyniki:
# Adres IP: 192.168.1.1
# Adres IP poprawny.

# Adres IP: 192.168.1
# Adres IP niepoprawny.


#Zadanie4
import sys
import socket

if len(sys.argv) != 2:
    sys.exit(1)

ip = sys.argv[1]

try:
    hostname = socket.gethostbyaddr(ip)
    print("Hostname:", hostname[0])
except socket.herror:
    print("Nie znaleziono nazwy hosta")
except socket.gaierror:
    print("Błąd w adresie IP")

# Wyniki:
# python main.py 1.1.1.1
# Hostname: one.one.one.one
#
# python main.py 8.8.8.8
# Hostname: dns.google


#Zadanie5
import sys
import socket

if len(sys.argv) != 2:
    sys.exit(1)

hostname = sys.argv[1]

try:
    ip = socket.gethostbyname(hostname)
    print("Adres IP:", ip)
except socket.gaierror:
    print("Niepoprawny hostname.")

# Wynik:
# python main.py localhost
# Adres IP: 127.0.0.1


#Zadanie6
import sys
import socket

if len(sys.argv) != 3:
    sys.exit(1)

host = sys.argv[1]
try:
    port = int(sys.argv[2])
except ValueError:
    print("Błąd w porcie")
    sys.exit(1)

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(5)
    s.connect((host, port))
    print(f"Udało się nawiązać połączenie {host} z portem {port}")
    s.close()
except socket.timeout:
    print("Przekroczono czas oczekiwania")
except Exception as e:
    print("Nie udało się nawiązać połączenia.")

# Wyniki:
# python main.py localhost 80
# Nie udało się nawiązać połączenia.

# python main.py localhost 135
# Udało się nawiązać połączenie localhost z portem 135


#Zadanie7
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
    s.settimeout(0.5)
    try:
        result = s.connect_ex((ip, port))
        if result == 0:
            print(f"Port {port} jest otwarty")
    except socket.error:
        pass
    finally:
        s.close()

print("\nSkanowanie zakończone")

# Wyniki:
# python main.py scanme.nmap.org
# Skanowanie
# Port 22 jest otwarty
# Port 80 jest otwarty
# Skanowanie zakńczone

# python main.py 45.33.32.156
# Skanowanie
# Port 22 jest otwarty
# Port 80 jest otwarty
# Skanowanie zakńczone