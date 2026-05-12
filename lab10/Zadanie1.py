import socket
import base64
import os

host = "127.0.0.1"
port = 8081
sciezka = "/.ws"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

klucz_losowy = base64.b64encode(os.urandom(16)).decode('utf-8')

zadanie = f"GET {sciezka} HTTP/1.1\r\n"
zadanie += f"Host: {host}:{port}\r\n"
zadanie += "Upgrade: websocket\r\n"
zadanie += "Connection: Upgrade\r\n"
zadanie += f"Sec-WebSocket-Key: {klucz_losowy}\r\n"
zadanie += "Sec-WebSocket-Version: 13\r\n\r\n"

print("Wysylam zapytanie Handshake do serwera")
sock.send(zadanie.encode())

odpowiedz = sock.recv(4096).decode('utf-8', errors='ignore')

print("\nOtrzymano odpowiedz od serwera:")
print(odpowiedz)

sock.close()


# Wyniki:
# Wysylam zapytanie Handshake do serwera...
# Otrzymano odpowiedz od serwera:
# HTTP/1.1 101 Switching Protocols
# Upgrade: websocket
# Connection: Upgrade
# Sec-WebSocket-Accept: VKo3RlKmfYsMIUPmEAT1MaPp04g=
