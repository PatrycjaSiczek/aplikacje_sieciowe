import socket

host = "httpbin.org"
port = 80
sciezka = "/image/png"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

zapytanie = f"GET {sciezka} HTTP/1.1\r\n"
zapytanie += f"Host: {host}\r\n"
zapytanie += "Connection: close\r\n\r\n"

print("Wysylam zapytanie GET o zasob /image/png")
sock.send(zapytanie.encode())

odpowiedz = b""
while True:
    fragment = sock.recv(4096)
    if not fragment:
        break
    odpowiedz += fragment

sock.close()

cialo_obrazka = odpowiedz.split(b"\r\n\r\n", 1)[1]

print("Zapisuje odebrane bajty jako plik obraz_zad2.png")
with open("obraz_zad2.png", "wb") as plik:
    plik.write(cialo_obrazka)

# Wyniki:
# Wysylam zapytanie GET o zasob /image/png
# Zapisuje odebrane bajty jako plik obraz_zad2.png