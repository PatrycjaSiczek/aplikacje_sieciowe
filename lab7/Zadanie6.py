import socket

def czytaj_linie(sock):
    dane = b""
    while not dane.endswith(b"\r\n"):
        dane += sock.recv(1)
    return dane.decode('utf-8')

adres = input("Podaj adres serwera: ")
port = int(input("Podaj port: "))
login = input("Podaj login: ")
haslo = input("Podaj haslo: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((adres, port))
czytaj_linie(sock)

sock.send(f"USER {login}\r\n".encode())
czytaj_linie(sock)
sock.send(f"PASS {haslo}\r\n".encode())
czytaj_linie(sock)

print("Pytanie serwera o skrzynke:")
sock.send(b"STAT\r\n")
odpowiedz = czytaj_linie(sock).strip()

czesci = odpowiedz.split()
liczba_wiadomosci = czesci[1]

print(f"\n W skrzynce znajduje sie: {liczba_wiadomosci} wiadomosci.")

sock.send(b"QUIT\r\n")
czytaj_linie(sock)
(sock.close())

# Wyniki:
# Podaj adres serwera: 127.0.0.1
# Podaj port: 1110
# Podaj login: pasinf2017@interia.pl
# Podaj haslo: P4SInf2017
# Pytanie serwera o skrzynke:
# W skrzynce znajduje sie: 17 wiadomosci.
# Process finished with exit code 0