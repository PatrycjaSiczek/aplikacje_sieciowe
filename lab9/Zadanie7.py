import socket
import os

HOST = '127.0.0.1'
PORT = 8080

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Serwer nasluchuje na {HOST}:{PORT}")

while True:
    conn, addr = server_socket.accept()
    print(f"\nPolaczono z klientem pod adresem {addr}")

    zadanie = conn.recv(1024).decode(errors='ignore')
    if not zadanie:
        conn.close()
        continue

    pierwsza_linia = zadanie.split('\r\n')[0]
    print(f"Zadanie od klienta: {pierwsza_linia}")

    czesci_zadania = pierwsza_linia.split()

    if len(czesci_zadania) < 2:
        print("Wykryto nieprawidlowa skladnie zapytania! Przesylam blad 400 Bad Request.")
        try:
            with open("400.html", "rb") as plik:
                zawartosc = plik.read()
            odpowiedz = b"HTTP/1.1 400 Bad Request\r\n"
            odpowiedz += b"Content-Type: text/html; charset=utf-8\r\n"
            odpowiedz += f"Content-Length: {len(zawartosc)}\r\n".encode()
            odpowiedz += b"Connection: close\r\n\r\n"
            odpowiedz += zawartosc
            conn.sendall(odpowiedz)
        except FileNotFoundError:
            print("Blad: Brak pliku 400.html w folderze!")

    else:
        sciezka = czesci_zadania[1]

        if sciezka == "/" or sciezka == "/index.html" or sciezka == "/index (1).html":
            print("Sciezka znana. Przesylam strone glowna (Kod 200 OK).")
            try:
                with open("index (1).html", "rb") as plik:
                    zawartosc = plik.read()
                odpowiedz = b"HTTP/1.1 200 OK\r\n"
                odpowiedz += b"Content-Type: text/html; charset=utf-8\r\n"
                odpowiedz += f"Content-Length: {len(zawartosc)}\r\n".encode()
                odpowiedz += b"Connection: close\r\n\r\n"
                odpowiedz += zawartosc
                conn.sendall(odpowiedz)
            except FileNotFoundError:
                print("Blad: Brak pliku index (1).html w folderze!")

        else:
            print("Nieznana sciezka. Przesylam strone bledu (Kod 404 Not Found).")
            try:
                with open("404.html", "rb") as plik:
                    zawartosc = plik.read()
                odpowiedz = b"HTTP/1.1 404 Not Found\r\n"
                odpowiedz += b"Content-Type: text/html; charset=utf-8\r\n"
                odpowiedz += f"Content-Length: {len(zawartosc)}\r\n".encode()
                odpowiedz += b"Connection: close\r\n\r\n"
                odpowiedz += zawartosc
                conn.sendall(odpowiedz)
            except FileNotFoundError:
                print("Blad: Brak pliku 404.html w folderze!")

    conn.close()
    print("Zakonczono obsluge klienta.")