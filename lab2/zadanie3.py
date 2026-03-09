import socket

if __name__ == '__main__':
    sockIPv4 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sockIPv4.settimeout(5)

    try:
        sockIPv4.connect(('212.182.24.27', 2900))
        while True:
            message = input("wpisz wiadomosc, jesli nie to exit ")
            if  message.lower() == 'exit': break
            sockIPv4.sendall(message.encode('utf-8'))
            response = sockIPv4.recv(1024)
            print(f"Odpowiedz serwera: {response.decode('utf-8')}")
    except socket.error as exc:
            print("Wyjatek socket.error : %s" % exc)
    sockIPv4.close()