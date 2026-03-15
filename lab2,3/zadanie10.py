import socket

address =('127.0.0.1', 2907)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)

try:
    hostname = input("Nazwa hosta  ")

    print(f"Pytanie o host: {hostname}")
    sock.sendto(hostname.encode('utf-8'), address)

    data, server = sock.recvfrom(1024)

    print(f"IP: {data.decode('utf-8')}")

except socket.timeout:
    print("Błąd timeout")
except Exception as e:
    print(f"błąd")
finally:
    sock.close()

#Wyniki:
# Nazwa hosta  www.google.com
# Pytanie o host: www.google.com
# IP: 142.250.120.104
#
# Serwer
# [2026-03-09 15:29:49] UDP DNS Server (Hostname -> IP) działa na porcie 2907...
# [2026-03-09 15:31:36] Zapytanie o: google od ('127.0.0.1', 50833)
# [2026-03-09 15:31:39] Nie znaleziono IP dla google
# [2026-03-09 15:31:51] Zapytanie o: www.google.com od ('127.0.0.1', 65498)
# [2026-03-09 15:31:51] Wysłano IP: 142.250.120.104

