import socket

def wyslij(gniazdo, komenda, tag):
    print(f"Wysylam do serwera: {komenda.strip()}")
    gniazdo.send(komenda.encode())
    pelna_odpowiedz = ""
    while True:
        dane = b""
        while not dane.endswith(b"\r\n"):
            dane += gniazdo.recv(1)
        linia = dane.decode('utf-8', errors='ignore')
        pelna_odpowiedz += linia
        if linia.startswith(tag + " OK") or linia.startswith(tag + " NO") or linia.startswith(tag + " BAD"):
            break
    return pelna_odpowiedz

adres = input("Podaj adres serwera IMAP: ")
port = int(input("Podaj port: "))
login = input("Podaj login: ")
haslo = input("Podaj haslo: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((adres, port))
powitanie = sock.recv(1024).decode()
print(f"Serwer: {powitanie.strip()}")

wyslij(sock, f"A1 LOGIN {login} {haslo}\r\n", "A1")

odpowiedz_status = wyslij(sock, "A2 STATUS INBOX (MESSAGES)\r\n", "A2")

for linia in odpowiedz_status.split('\r\n'):
    if "MESSAGES" in linia:
        liczba = linia.split("MESSAGES")[1].replace(")", "").strip()
        print(f"W skrzynce INBOX znajduje sie {liczba} wiadomosci.")

wyslij(sock, "A3 LOGOUT\r\n", "A3")
sock.close()

#Wynik:
# Podaj adres serwera IMAP: 127.0.0.1
# Podaj port: 1143
# Podaj login: pasumcs@infumcs.edu
# Podaj haslo: P4SInf2017
# Serwer: * OK IMAP4rev1 Service Ready
# Wysylam do serwera: A1 LOGIN pasumcs@infumcs.edu P4SInf2017
# Wysylam do serwera: A2 STATUS INBOX (MESSAGES)
# W skrzynce INBOX znajduje sie 5 wiadomosci.
# Wysylam do serwera: A3 LOGOUT

