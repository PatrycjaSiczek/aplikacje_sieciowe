import socket
import base64
import os

host = "127.0.0.1"
port = 8081
sciezka = "/.ws"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

klucz_losowy = base64.b64encode(os.urandom(16)).decode('utf-8')
zadanie = f"GET {sciezka} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {klucz_losowy}\r\nSec-WebSocket-Version: 13\r\n\r\n"

sock.send(zadanie.encode())
sock.recv(4096)
print("Handshake przebiegł pomyslnie. Skladam ramke")

wiadomosc = b"Witaj serwerze! To jest krotka wiadomosc."
dlugosc = len(wiadomosc)

ramka = bytearray()
ramka.append(0x81)
ramka.append(0x80 | dlugosc)

klucz_maskujacy = os.urandom(4)
ramka.extend(klucz_maskujacy)

for i in range(dlugosc):
    zamaskowany_bajt = wiadomosc[i] ^ klucz_maskujacy[i % 4]
    ramka.append(zamaskowany_bajt)

print(f"Wysylam ramke z maskowanymi danymi rozmiar danych: {dlugosc}")
sock.send(ramka)

odpowiedz_serwera = sock.recv(4096)
print(f"Odebrano dane od serwera: {odpowiedz_serwera}")

sock.close()

# Wyniki:
# Handshake przebiegł pomyslnie. Skladam ramke
# Wysylam ramke z maskowanymi danymi rozmiar danych: 41
# Odebrano dane od serwera: b'\x81)Witaj serwerze! To jest krotka wiadomosc.'


