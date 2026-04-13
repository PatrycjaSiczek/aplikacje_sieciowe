import socket

def odbierz(gniazdo, znacznik):
    dane = b""
    while not dane.endswith(znacznik):
        dane += gniazdo.recv(1)
    return dane.decode('utf-8', errors='ignore')

adres = input("Podaj adres serwera: ")
port = int(input("Podaj port: "))
login = input("Podaj login: ")
haslo = input("Podaj haslo: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((adres, port))
odbierz(sock, b"\r\n")

sock.send(f"USER {login}\r\n".encode())
odbierz(sock, b"\r\n")
sock.send(f"PASS {haslo}\r\n".encode())
odbierz(sock, b"\r\n")

sock.send(b"STAT\r\n")
odpowiedz_stat = odbierz(sock, b"\r\n")
liczba_wiadomosci = int(odpowiedz_stat.split()[1])

print(f"Wykryto {liczba_wiadomosci} wiadomosci.")

for i in range(1, liczba_wiadomosci + 1):
    print(f"\nPobieranie wiadomosci {i} ---")
    sock.send(f"RETR {i}\r\n".encode())

    status = odbierz(sock, b"\r\n")

    if status.startswith("+OK"):
        tresc = odbierz(sock, b"\r\n.\r\n")
        print(f"Status: {status.strip()}")
        print(tresc)
    else:
        print(f"Serwer zwrocil blad dla tej wiadomosci: {status.strip()}")
        print("Pomijam i ide do kolejnej...")

print("\nWszystkie wiadomosci zostaly przetworzone.")
sock.send(b"QUIT\r\n")
odbierz(sock, b"\r\n")
sock.close()

# Wyniki:
# Podaj adres serwera: 127.0.0.1
# Podaj port: 1110
# Podaj login: pasinf2017@interia.pl
# Podaj haslo: P4SInf2017
# Wykryto 17 wiadomosci.
#
# Pobieranie wiadomości 1
# Status: +OK 100 octets
# From: nadawca1@serwer.pl
# To: pasinf2017@interia.pl
# Subject: Wygenerowana wiadomosc 1
#
# To jest automatyczna tresc wiadomosci numer 1.
# .
#
#
# Pobieranie wiadomości 2
# Status: +OK 100 octets
# From: nadawca2@serwer.pl
# To: pasinf2017@interia.pl
# Subject: Wygenerowana wiadomosc 2
#
# To jest automatyczna tresc wiadomosci numer 2.
# .
#
#
# Pobieranie wiadomości 3
# Status: +OK 100 octets
# From: nadawca3@serwer.pl
# To: pasinf2017@interia.pl
# Subject: Wygenerowana wiadomosc 3
#
# To jest automatyczna tresc wiadomosci numer 3.
# .
#
#
# Pobieranie wiadomości 4
# Status: +OK 100 octets
# From: nadawca4@serwer.pl
# To: pasinf2017@interia.pl
# Subject: Wygenerowana wiadomosc 4
#
# To jest automatyczna tresc wiadomosci numer 4.
# .
#
#
# Pobieranie wiadomości 5
# Status: +OK 100 octets
# From: nadawca5@serwer.pl
# To: pasinf2017@interia.pl
# Subject: Wygenerowana wiadomosc 5
#
# To jest automatyczna tresc wiadomosci numer 5.
# .
#
#
# Pobieranie wiadomości 6
# Status: +OK 100 octets
# From: nadawca6@serwer.pl
# To: pasinf2017@interia.pl
# Subject: Wygenerowana wiadomosc 6
#
# To jest automatyczna tresc wiadomosci numer 6.
# .
#
#
# Pobieranie wiadomości 7
# Status: +OK 100 octets
# From: nadawca7@serwer.pl
# To: pasinf2017@interia.pl
# Subject: Wygenerowana wiadomosc 7
#
# To jest automatyczna tresc wiadomosci numer 7.
# .
#
#
# Pobieranie wiadomości 8
# Status: +OK 1257 octets
# From: test@interia.pl
# Subject: Test
#
# Tresc wiadomosci numer 8
# .
#
#
# Pobieranie wiadomości 9
# Status: +OK 100 octets
# From: nadawca9@serwer.pl
# To: pasinf2017@interia.pl
# Subject: Wygenerowana wiadomosc 9
#
# To jest automatyczna tresc wiadomosci numer 9.
# .
#
#
# Pobieranie wiadomości 10
# Status: +OK 100 octets
# From: nadawca10@serwer.pl
# To: pasinf2017@interia.pl
# Subject: Wygenerowana wiadomosc 10
#
# To jest automatyczna tresc wiadomosci numer 10.
# .
#
#
# Pobieranie wiadomości 11
# Status: +OK 50 octets
# From: spam@spam.pl
# Subject: Najmniejsza
#
# To jest najmniejsza wiadomosc
# .
#
# Pobieranie wiadomości 12
# Status: +OK 100 octets
# From: nadawca12@serwer.pl
# To: pasinf2017@interia.pl
# Subject: Wygenerowana wiadomosc 12
#
# To jest automatyczna tresc wiadomosci numer 12.
#
# .
#
# Pobieranie wiadomości 13
# Status: +OK 100 octets
# From: nadawca13@serwer.pl
# To: pasinf2017@interia.pl
# Subject: Wygenerowana wiadomosc 13
#
# To jest automatyczna tresc wiadomosci numer 13.
# .
#
#
# Pobieranie wiadomości 14
# Status: +OK 100 octets
# From: nadawca14@serwer.pl
# To: pasinf2017@interia.pl
# Subject: Wygenerowana wiadomosc 14
#
# To jest automatyczna tresc wiadomosci numer 14.
#
# .
#
#
# Pobieranie wiadomości 15
# Status: +OK 100 octets
# From: nadawca15@serwer.pl
# To: pasinf2017@interia.pl
# Subject: Wygenerowana wiadomosc 15
#
# To jest automatyczna tresc wiadomosci numer 15.
#
# .
#
#
# Pobieranie wiadomości 16
# Status: +OK 100 octets
# From: nadawca16@serwer.pl
# To: pasinf2017@interia.pl
# Subject: Wygenerowana wiadomosc 16
#
# To jest automatyczna tresc wiadomosci numer 16.
# .
#
# Pobieranie wiadomości 17
# Status: +OK 2376 octets
# From: wykladowca@uczelnia.pl
# Subject: Najwieksza
# abdgdfgffd -
# To jest najwieksza wiadomosc w calej skrzynce.
# .
#
# Wszystkie wiadomosci zostaly przetworzone.
# Process finished with exit code 0
