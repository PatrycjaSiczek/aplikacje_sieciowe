import socket

host = "httpbin.org"
port = 80
sciezka = "/post"

imie = input("Wypelnij pole 'imie': ")
nazwisko = input("Wypelnij pole 'nazwisko': ")

dane_formularza = f"imie={imie}&nazwisko={nazwisko}"
dlugosc_danych = len(dane_formularza.encode('utf-8'))

zapytanie = f"POST {sciezka} HTTP/1.1\r\n"
zapytanie += f"Host: {host}\r\n"
zapytanie += "Content-Type: application/x-www-form-urlencoded\r\n"
zapytanie += f"Content-Length: {dlugosc_danych}\r\n"
zapytanie += "Connection: close\r\n\r\n"
zapytanie += dane_formularza

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
sock.send(zapytanie.encode('utf-8'))

odpowiedz = b""
while True:
    fragment = sock.recv(4096)
    if not fragment:
        break
    odpowiedz += fragment

sock.close()

cialo_odpowiedzi = odpowiedz.split(b"\r\n\r\n", 1)[1].decode()
print("\n Odpowiedz Serwera w obiekcie JSON")
print(cialo_odpowiedzi)

# Wyniki:
# Wypelnij pole 'imie': Patrycja
# Wypelnij pole 'nazwisko': Siczek
#
#  Odpowiedz Serwera w obiekcie JSON
# {
#   "args": {},
#   "data": "",
#   "files": {},
#   "form": {
#     "imie": "Patrycja",
#     "nazwisko": "Siczek"
#   },
#   "headers": {
#     "Content-Length": "29",
#     "Content-Type": "application/x-www-form-urlencoded",
#     "Host": "httpbin.org",
#     "X-Amzn-Trace-Id": "Root=1-6a01cda0-0c8f333c055b231e176d5102"
#   },
#   "json": null,
#   "origin": "213.134.172.80",
#   "url": "http://httpbin.org/post"
# }
