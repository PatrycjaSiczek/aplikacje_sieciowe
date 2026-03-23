import socket
import random


def start_server():
    server_ip = "127.0.0.1"
    server_port = 2912
    secret_number = random.randint(1, 100)

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((server_ip, server_port))
    server.listen(1)

    print(f"Serwer czeka na połączenie... (Wylosowana: {secret_number})")
    conn, addr = server.accept()
    print(f"Połączono z: {addr}")

    with conn:
        while True:
            data = conn.recv(1024).decode('utf-8').strip()
            if not data: break

            if not data.isdigit():
                conn.send("BŁĄD: Podaj poprawną liczbę!".encode('utf-8'))
                continue

            val = int(data)
            if val < secret_number:
                conn.send("Liczba jest większa.".encode('utf-8'))
            elif val > secret_number:
                conn.send("Liczba jest mniejsza.".encode('utf-8'))
            else:
                conn.send("Zgadles!".encode('utf-8'))
                break

    server.close()


if __name__ == "__main__":
    start_server()

# Wyniki:
# Połączono z serwerem.
# Podaj liczbę: 4
# Serwer mówi: Liczba jest większa.
# Podaj liczbę: 40
# Serwer mówi: Liczba jest mniejsza.
# Podaj liczbę: 38
# Serwer mówi: Liczba jest mniejsza.
# Podaj liczbę: 20
# Serwer mówi: Liczba jest mniejsza.
# Podaj liczbę: 10
# Serwer mówi: Liczba jest większa.
# Podaj liczbę: 15
# Serwer mówi: Zgadles!
# Podaj liczbę: