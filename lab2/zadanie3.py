import socket

if __name__ == '__main__':
    sockIPv4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockIPv4.settimeout(5)

    try:
        sockIPv4.connect(('127.0.0.1', 2900))
        while True:
            message = input("wpisz wiadomosc, jesli nie to exit ")
            if  message.lower() == 'exit': break
            sockIPv4.sendall(message.encode('utf-8'))
            response = sockIPv4.recv(1024)
            print(f"Odpowiedz serwera: {response.decode('utf-8')}")
    except socket.error as exc:
            print("Wyjatek socket.error : %s" % exc)
    sockIPv4.close()

    # Wyniki:
    # wpisz wiadomosc, jesli nie to exit Hello
    # Odpowiedz serwera: Hello
    # wpisz wiadomosc,jesli nie to exit HI
    # Odpowiedz serwera: HI
    # wpisz wiadomosc, jesli nie to exit exit
    #
    # Serwer:
    # Serwer ECHO uruchomiony na 127.0.0.1:2900
    # Oczekiwanie na polaczenia...
    # [2026-03-09 12:14:16] Klient ('127.0.0.1', 51192) polaczyl sie.
    # [2026-03-09 12:14:25] Odeslano do ('127.0.0.1', 51192): Hello
    # [2026-03-09 12:14:30] Odeslano do ('127.0.0.1', 51192): HI
    # [2026-03-09 12:14:48] Klient rozlaczyl sie.


