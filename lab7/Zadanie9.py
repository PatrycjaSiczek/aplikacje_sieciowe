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

sock.send(b"LIST\r\n")
lista = odbierz(sock, b"\r\n.\r\n").split('\r\n')[1:-2]

najwiekszy_numer = ""
najwiekszy_rozmiar = 0

for linia in lista:
    numer, rozmiar = linia.split()
    rozmiar_liczba = int(rozmiar)
    if rozmiar_liczba > najwiekszy_rozmiar:
        najwiekszy_rozmiar = rozmiar_liczba
        najwiekszy_numer = numer

print(f"Najwieksza wiadomosc to nr {najwiekszy_numer} - {najwiekszy_rozmiar} bajtow.")

sock.send(f"RETR {najwiekszy_numer}\r\n".encode())
tresc = odbierz(sock, b"\r\n.\r\n")

print("\nTresc wiadomosci:")
print(tresc)

sock.send(b"QUIT\r\n")
odbierz(sock, b"\r\n")
sock.close()

#Wyniki:
# Podaj adres serwera: 127.0.0.1
# Podaj port: 1110
# Podaj login: pasinf2017@interia.pl
# Podaj haslo: P4SInf2017
# Najwieksza wiadomosc to nr 17 - 2376 bajtow.
#
# Tresc wiadomosci:
# +OK 2376 octets
# From: wykladowca@uczelnia.pl
# To: pasinf2017@interia.pl
# Subject: Zadanie 4 - Najwieksza
#
# To jest tresc wiadomosci o najwiekszym rozmiarze w skrzynce.

