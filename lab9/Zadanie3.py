import socket

host = "httpbin.org"
port = 80
sciezka = "/image/jpeg"

zakresy = [(0, 10000), (10001, 20000), (20001, 36000)]
pelny_obrazek = b""

for i, (poczatek, koniec) in enumerate(zakresy):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))

    zapytanie = f"GET {sciezka} HTTP/1.1\r\n"
    zapytanie += f"Host: {host}\r\n"
    zapytanie += f"Range: bytes={poczatek}-{koniec}\r\n"
    zapytanie += "Connection: close\r\n\r\n"

    print(f"Wysylam zapytanie o czesc nr {i + 1} bajty {poczatek}-{koniec}")
    sock.send(zapytanie.encode())

    odpowiedz = b""
    while True:
        dane = sock.recv(4096)
        if not dane:
            break
        odpowiedz += dane

    sock.close()

    fragment_obrazka = odpowiedz.split(b"\r\n\r\n", 1)[1]
    pelny_obrazek += fragment_obrazka
    print(f"Pobrano {len(fragment_obrazka)} bajtow.")

print("Zapis jako obraz_zad3.jpg.")
with (open("obraz_zad3.jpg", "wb") as plik):
    plik.write(pelny_obrazek)

#Wyniki:
# Wysylam zapytanie o czesc nr 1 bajty 0-10000
# Pobrano 35588 bajtow.
# Wysylam zapytanie o czesc nr 2 bajty 10001-20000
# Pobrano 35588 bajtow.
# Wysylam zapytanie o czesc nr 3 bajty 20001-36000
# Pobrano 35588 bajtow.
# Zpis jako obraz_zad3.jpg.