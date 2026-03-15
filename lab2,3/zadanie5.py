import socket

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(5)

    try:
        server = ('127.0.0.1', 2901)
        while True:
            message = input("wpisz wiadomosc ")
            if  message.lower() == 'exit': break
            sock.sendto(message.encode('utf-8'), server)
            data = sock.recv(1024)
            print(f"Odpowiedz serwera: {data.decode('utf-8')}")
    except socket.error as exc:
            print("Wyjatek socket.error : %s" % exc)
    finally:
        print("Zamkniecie gniazda")
        sock.close()

# Wyniki:
# wpisz wiadomosc abc
# Odpowiedz serwera: abc
# wpisz wiadomosc exit
# Zamkniecie gniazda
#
# Serwer:
# [2026-03-09 12:31:43] UDP ECHO Server działa na 127.0.0.1:2901
# Oczekiwanie na dane od klienta..
# [2026-03-09 12:32:55] Odebrano od ('127.0.0.1', 63206): abc
# [2026-03-09 12:32:55] Odesłano 3 bajtów echo do ('127.0.0.1', 63206)