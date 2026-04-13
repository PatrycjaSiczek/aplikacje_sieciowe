import socket

def odbierz(gniazdo, znacznik):
    dane = b""
    while not dane.endswith(znacznik):
        dane += gniazdo.recv(1)
    return dane.decode('utf-8', errors='ignore')

adres = input("Podaj adres serwera: ")
port = int(input("Podaj port (np. 1110): "))
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
odpowiedz_list = odbierz(sock, b"\r\n.\r\n")

print("\nWynik dzialania serwera:")
linie = odpowiedz_list.split('\r\n')
for linia in linie[1:-2]:
    elementy = linia.split()
    print(f"Wiadomosc numer {elementy[0]} -  {elementy[1]} bajtow.")

sock.send(b"QUIT\r\n")
odbierz(sock, b"\r\n")
sock.close()

# Wyniki:
# Podaj adres serwera: 127.0.11100.1
# Podaj port (np. 1110): 1110
# Podaj login: pasinf2017@interia.pl
# Podaj haslo: P4SInf2017
#
# Wynik dzialania serwera:
# Wiadomosc numer 1 -  1321 bajtow.
# Wiadomosc numer 2 -  1319 bajtow.
# Wiadomosc numer 3 -  1319 bajtow.
# Wiadomosc numer 4 -  1337 bajtow.
# Wiadomosc numer 5 -  1311 bajtow.
# Wiadomosc numer 6 -  1255 bajtow.
# Wiadomosc numer 7 -  1255 bajtow.
# Wiadomosc numer 8 -  1257 bajtow.
# Wiadomosc numer 9 -  1255 bajtow.
# Wiadomosc numer 10 -  1255 bajtow.
# Wiadomosc numer 11 -  1253 bajtow.
# Wiadomosc numer 12 -  1255 bajtow.
# Wiadomosc numer 13 -  1257 bajtow.
# Wiadomosc numer 14 -  1255 bajtow.
# Wiadomosc numer 15 -  1311 bajtow.
# Wiadomosc numer 16 -  1255 bajtow.
# Wiadomosc numer 17 -  2376 bajtow.