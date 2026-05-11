import socket

host = "httpbin.org"
port = 80
sciezka = "/image/jpeg"

zapytanie = f"GET {sciezka} HTTP/1.1\r\n"
zapytanie += f"Host: {host}\r\n"
zapytanie += "If-Modified-Since: Wed, 21 Oct 2030 07:28:00 GMT\r\n"
zapytanie += "Connection: close\r\n\r\n"

print("Wysylam zapytanie z naglowkiem If-Modified-Since")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
sock.send(zapytanie.encode())

odpowiedz = b""
while True:
    fragment = sock.recv(4096)
    if not fragment:
        break
    odpowiedz += fragment

sock.close()

naglowki = odpowiedz.split(b"\r\n\r\n", 1)[0].decode()
pierwsza_linia = naglowki.split('\r\n')[0]

print("\nOtrzymana odpowiedz z serwera:")
print(pierwsza_linia)

if "304" in pierwsza_linia:
    print("Serwer zwrocil kod 304! Plik nie ulegl zmianie, nie pobieramy ciala.")
else:
    print("Zapisuje nowa wersje.")
    cialo = odpowiedz.split(b"\r\n\r\n", 1)[1]
    with open("obraz_zad6.jpg", "wb") as plik:
        plik.write(cialo)

# Wyniki:
# Wysylam zapytanie z naglowkiem If-Modified-Since
#
# Otrzymana odpowiedz z serwera:
# HTTP/1.1 200 OK
# Zapisuje nowa wersje.

