import socket

def wyslij(gniazdo, komenda, tag):
    print(f"Wysylam: {komenda.strip()}")
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
numer_do_usuniecia = input("Podaj numer wiadomosci, ktora chcesz zniszczyc: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((adres, port))
sock.recv(1024)

wyslij(sock, f"A1 LOGIN {login} {haslo}\r\n", "A1")
wyslij(sock, "A2 SELECT INBOX\r\n", "A2")

print(f"Wiadomosc {numer_do_usuniecia} flaga \Deleted")
wyslij(sock, f"A3 STORE {numer_do_usuniecia} +FLAGS (\\Deleted)\r\n", "A3")

print("Fizyczne kasowanie")
wyslij(sock, "A4 EXPUNGE\r\n", "A4")

print("Wiadomosc usunieta")

wyslij(sock, "A5 LOGOUT\r\n", "A5")
sock.close()

# Wyniki:
# Podaj adres serwera IMAP: 127.0.0.1
# Podaj port: 1143
# Podaj login: pasumcs@infumcs.edu
# Podaj haslo: P4SInf2017
# Podaj numer wiadomosci, ktora chcesz zniszczyc: 1
# Wysylam: A1 LOGIN pasumcs@infumcs.edu P4SInf2017
# Wysylam: A2 SELECT INBOX
# Wiadomosc 1 flaga \Deleted
# Wysylam: A3 STORE 1 +FLAGS (\Deleted)
# Fizyczne kasowanie
# Wysylam: A4 EXPUNGE
# Wiadomosc usunieta
# Wysylam: A5 LOGOUT
