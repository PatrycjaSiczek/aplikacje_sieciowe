import socket
import base64
def odbierz(gniazdo, znacznik):
    dane = b""
    while not dane.endswith(znacznik):
        dane += gniazdo.recv(1)
    return dane.decode('utf-8', errors='ignore')

adres = input("Podaj adres serwera: ")
port = int(input("Podaj port: "))
login = input("Podaj login: ")
haslo = input("Podaj haslo: ")
numer = input("Podaj numer wiadomosci z zalacznikiem: ")

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((adres, port))
odbierz(sock, b"\r\n")

sock.send(f"USER {login}\r\n".encode())
odbierz(sock, b"\r\n")
sock.send(f"PASS {haslo}\r\n".encode())
odbierz(sock, b"\r\n")

print(f"Pobieram wiadomosc nr {numer}...")
sock.send(f"RETR {numer}\r\n".encode())
tresc = odbierz(sock, b"\r\n.\r\n")

sock.send(b"QUIT\r\n")
sock.close()

linie = tresc.split('\r\n')
kod_base64 = ""
nazwa_pliku = "obraz.gif"
w_trakcie_zalacznika = False

for linia in linie:
    if "filename=" in linia:
        nazwa_pliku = linia.split('filename=')[1].replace('"', '').replace(';', '').strip()
        print(f"Nazwe pliku: {nazwa_pliku}")

    if w_trakcie_zalacznika:
        if linia.startswith("--") or linia == ".":
            break
        kod_base64 += linia

    if "Content-Transfer-Encoding: base64" in linia:
        w_trakcie_zalacznika = True
        print("Odczyt danych z Base64")

if kod_base64:
    print(f"Zapisuje plik pod nazwa {nazwa_pliku}")
    dane_binarne = base64.b64decode(kod_base64)
    with open(nazwa_pliku, 'wb') as plik:
        plik.write(dane_binarne)
    print("Plik zostal zapisany w folderze projektu.")
else:
    print("Błąd nie znaleziono zalacznika.")

#Wyniki:
# Podaj adres serwera: 127.0.0.1
# Podaj port: 1110
# Podaj login: pasinf2017@interia.pl
# Podaj haslo: P4SInf2017
# Podaj numer wiadomosci z zalacznikiem: 3
# Pobieram wiadomosc nr 3
# Nazwe pliku: zad11.gif
# Odczyt danych z Base64
# Zapisuje plik pod nazwa zad11.gif
# Plik zostal zapisany w folderze projektu.
