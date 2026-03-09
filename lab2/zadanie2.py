import socket

if __name__ == '__main__':
    sockIPv4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockIPv4.settimeout(5)
    message = "Hello World"
    try:
        sockIPv4.connect(('127.0.0.1', 2900))
        sockIPv4.sendall(message.encode('utf-8'))
        response = sockIPv4.recv(1024)
        print(f"Odpowiedz serwera: {response.decode('utf-8')}")
    except socket.error as exc:
            print("Wyjatek socket.error : %s" % exc)
    sockIPv4.close()

    # Wyniki
    # Odpowiedz serwera: Hello World
    # Serwer:
    # Oczekiwanie na polaczenia...
    # [2026-03-09 12:21:15] Klient ('127.0.0.1', 64068) polaczyl sie.
    # [2026-03-09 12:21:15] Odeslano do ('127.0.0.1', 64068): Hello World
    # [2026-03-09 12:21:15] Klient rozlaczyl sie.

