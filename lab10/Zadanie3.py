import socket
import base64
import os
import struct

host = "127.0.0.1"
port = 8081
sciezka = "/.ws"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

klucz_losowy = base64.b64encode(os.urandom(16)).decode('utf-8')
zadanie = f"GET {sciezka} HTTP/1.1\r\nHost: {host}:{port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: {klucz_losowy}\r\nSec-WebSocket-Version: 13\r\n\r\n"

sock.send(zadanie.encode())
sock.recv(4096)
print("Handshake przebiegł pomyslnie.")

wiadomosc = b"A" * 300
dlugosc = len(wiadomosc)

print(f"Przygotowuje bardzo dluga wiadomosc o rozmiarze {dlugosc} bajtow.")

ramka = bytearray()
ramka.append(0x81)
ramka.append(0x80 | 126)
ramka.extend(struct.pack("!H", dlugosc))

klucz_maskujacy = os.urandom(4)
ramka.extend(klucz_maskujacy)

for i in range(dlugosc):
    zamaskowany_bajt = wiadomosc[i] ^ klucz_maskujacy[i % 4]
    ramka.append(zamaskowany_bajt)

print("Wysylam rozszerzona ramke")
sock.send(ramka)

odpowiedz_serwera = sock.recv(4096)
print(f"Odebrano dane od serwera zakodowana ramka: {odpowiedz_serwera[:20]} i wiecej.")

sock.close()

# Wyniki:
# Handshake przebiegł pomyslnie.
# Przygotowuje bardzo dluga wiadomosc o rozmiarze 300 bajtow.
# Wysylam rozszerzona ramke
# Odebrano dane od serwera zakodowana ramka: b'\x81^\nAAKAAKAAKAAKAAKAA' i wiecej.
