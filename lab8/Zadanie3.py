import socket

def wyslij(gniazdo, komenda, tag):
    print(f"Wysylam: {komenda.strip()}")
    gniazdo.send(komenda.encode())
    odpowiedz = ""
    while True:
        dane = b""
        while not dane.endswith(b"\r\n"):
            dane += gniazdo.recv(1)
        linia = dane.decode('utf-8', errors='ignore')
        odpowiedz += linia
        if linia.startswith(tag + " OK") or linia.startswith(tag + " NO") or linia.startswith(tag + " BAD"):
            break
    return odpowiedz

adres = input("Podaj adres serwera IMAP: ")
port = int(input("Podaj port: "))
login = input("Podaj login: ")
haslo = input("Podaj haslo: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((adres, port))
sock.recv(1024)

wyslij(sock, f"A1 LOGIN {login} {haslo}\r\n", "A1")

lista = wyslij(sock, "A2 LIST \"\" \"*\"\r\n", "A2")

skrzynki = []
for linia in lista.split('\r\n'):
    if linia.startswith("* LIST"):
        nazwa = linia.split('\"')[-2]
        if nazwa != "":
            skrzynki.append(nazwa)

liczba_wiadomosci = 0
tag_licznik = 3

for i in skrzynki:
    tag = f"A{tag_licznik}"
    print(f"Sprawdzam skrzynke: {i}")
    odpowiedz_status = wyslij(sock, f"{tag} STATUS \"{i}\" (MESSAGES)\r\n", tag)

    for linia in odpowiedz_status.split('\r\n'):
        if "MESSAGES" in linia:
            liczba = int(linia.split("MESSAGES")[1].replace(")", "").strip())
            print(f"Znaleziono {liczba} wiadomosci w folderze {i}.")
            liczba_wiadomosci += liczba

    tag_licznik += 1

print(f"\nLACZNIE na calym koncie masz {liczba_wiadomosci} wiadomosci.")

wyslij(sock, f"A{tag_licznik} LOGOUT\r\n", f"A{tag_licznik}")
sock.close()


# Wyniki:
# Podaj adres serwera IMAP: 127.0.0.1
# Podaj port: 1143
# Podaj login: pasumcs@infumcs.edu
# Podaj haslo: P4SInf2017
# Wysylam: A1 LOGIN pasumcs@infumcs.edu P4SInf2017
# Wysylam: A2 LIST "" "*"
# Sprawdzam skrzynke: INBOX
# Wysylam: A3 STATUS "INBOX" (MESSAGES)
# Znaleziono 5 wiadomosci w folderze INBOX.
# Sprawdzam skrzynke: Sent
# Wysylam: A4 STATUS "Sent" (MESSAGES)
# Znaleziono 2 wiadomosci w folderze Sent.
#
# LACZNIE na calym koncie masz 7 wiadomosci.
# Wysylam: A5 LOGOUT
#
# Process finished with exit code 0