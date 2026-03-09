import socket

if __name__ == '__main__':
    sockIPv4 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


    sockIPv4.settimeout(5)
    message = "Hello World"
    try:
        sockIPv4.connect(('127.0.0.1', 2901))
        sockIPv4.sendall(message.encode('utf-8'))
        response = sockIPv4.recv(1024)
        print(f"Odpowiedz serwera: {response.decode('utf-8')}")
    except socket.error as exc:
            print("Wyjatek socket.error : %s" % exc)
    sockIPv4.close()

# Wyniki:
# Odpowiedz serwera: Hello World
# Serwer:
# [2026-03-09 12:28:33] Serwer UDP ECHO dziala na 127.0.0.1:2901
# Oczekiwanie na wiadomosci od klienta...
# [2026-03-09 12:28:37] Odebrano od ('127.0.0.1', 62528): Hello World
# [2026-03-09 12:28:37] Odeslano echo do ('127.0.0.1', 62528)