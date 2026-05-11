import socket

host = "httpbin.org"
port = 80
sciezka = "/html"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

zapytanie = f"GET {sciezka} HTTP/1.1\r\n"
zapytanie += f"Host: {host}\r\n"
zapytanie += "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14\r\n"
zapytanie += "Connection: close\r\n\r\n"

print("Wysylam zadanie GET z naglowkiem User-Agent")
sock.send(zapytanie.encode())

odpowiedz_bajtowa = b""
while True:
    dane = sock.recv(4096)
    if not dane:
        break
    odpowiedz_bajtowa += dane

sock.close()

print("Odebrano dane od serwera. Oddzielam naglowki od ciala strony")
podzial = odpowiedz_bajtowa.split(b"\r\n\r\n", 1)
naglowki = podzial[0].decode()
cialo_html = podzial[1]

print("\n Otrzymane naglowki serwera")
print(naglowki)

print("\nZapisuje strone do pliku strona_zad1.html")
with open("strona_zad1.html", "wb") as plik:
    plik.write(cialo_html)


# Wyniki:
# Wysylam zadanie GET z naglowkiem User-Agent
# Odebrano dane od serwera. Oddzielam naglowki od ciala strony
#
#  Otrzymane naglowki serwera
# HTTP/1.1 200 OK
# Date: Mon, 11 May 2026 12:25:19 GMT
# Content-Type: text/html; charset=utf-8
# Content-Length: 3741
# Connection: close
# Server: gunicorn/19.9.0
# Access-Control-Allow-Origin: *
# Access-Control-Allow-Credentials: true
#
# Zapisuje strone do pliku strona_zad1.html
