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

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((adres, port))
sock.recv(1024)

wyslij(sock, f"A1 LOGIN {login} {haslo}\r\n", "A1")
wyslij(sock, "A2 SELECT INBOX\r\n", "A2")

print("Serach unseen")
odpowiedz_search = wyslij(sock, "A3 SEARCH UNSEEN\r\n", "A3")

numery_nieprzeczytanych = []
for linia in odpowiedz_search.split('\r\n'):
    if linia.startswith("* SEARCH"):
        czesci = linia.split()
        numery_nieprzeczytanych = czesci[2:]

if not numery_nieprzeczytanych:
    print("Brak nieprzeczytanych wiadomosci!")
else:
    print(f"Znaleziono nieprzeczytane wiadomosci: {numery_nieprzeczytanych}")
    tag_licznik = 4
    for numer in numery_nieprzeczytanych:
        print(f"\nPobieranie tresci wiadomosci {numer}")
        tresc = wyslij(sock, f"A{tag_licznik} FETCH {numer} BODY[]\r\n", f"A{tag_licznik}")
        print(tresc)
        tag_licznik += 1

        print(f"Wiadomosc {numer} Flaga - Seen")
        wyslij(sock, f"A{tag_licznik} STORE {numer} +FLAGS (\\Seen)\r\n", f"A{tag_licznik}")
        tag_licznik += 1

wyslij(sock, "A99 LOGOUT\r\n", "A99")
sock.close()

# Wynik:
# Podaj adres serwera IMAP: 127.0.0.1
# Podaj port: 1143
# Podaj login: pasumcs@infumcs.edu
# Podaj haslo: P4SInf2017
# Wysylam: A1 LOGIN pasumcs@infumcs.edu P4SInf2017
# Wysylam: A2 SELECT INBOX
# Serach unseen
# Wysylam: A3 SEARCH UNSEEN
# Znaleziono nieprzeczytane wiadomosci: ['2', '4']
# Pobieranie tresci wiadomosci 2
# Wysylam: A4 FETCH 2 BODY[]
# * 2 FETCH (BODY[] {50}
# To jest tresc wiadomosci IMAP z testowego serwera.
# )
# A4 OK FETCH completed
# Wiadomosc 2 Flaga - Seen
# Wysylam: A5 STORE 2 +FLAGS (\Seen)
# Pobieranie tresci wiadomosci 4
# Wysylam: A6 FETCH 4 BODY[]
# * 4 FETCH (BODY[] {50}
# To jest tresc wiadomosci IMAP z testowego serwera.
# )
# A6 OK FETCH completed
# Wiadomosc 4 Flaga - Seen
# Wysylam: A7 STORE 4 +FLAGS (\Seen)
# Wysylam: A99 LOGOUT
# Process finished with exit code 0