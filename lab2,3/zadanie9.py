import socket

server_address = ('127.0.0.1 ', 2906)
ip = "8.8.8.8"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)

try:
    print(f"IP: {ip}")
    sock.sendto(ip.encode('utf-8'), server_address)
    data, server = sock.recvfrom(1024)
    print(f"host {server}): {data.decode('utf-8')}")

except socket.timeout:
        print("Błąd: timeout")
except Exception as e:
        print(f"błąd")
finally:
    sock.close()

# Wyniki:
# IP: 8.8.8.8
# host ('127.0.0.1', 2906)): dns.google
# serwer:
# [2026-03-09 12:52:22] UDP DNS Server czeka na IP na porcie 2906...
# [2026-03-09 12:52:44] Otrzymano zapytanie o IP: 8.8.8.8 od ('127.0.0.1', 64380)
# [2026-03-09 12:52:49] Wysłano hostname: dns.google

