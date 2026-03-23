import socket

SERVER_IP = "127.0.0.1"
SERVER_PORT = 2912

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((SERVER_IP, SERVER_PORT))
    print("Połączono z serwerem.")

    while True:
        guess = input("Podaj liczbę: ")
        if guess.lower() == 'q':
            break

        sock.send(guess.encode('utf-8'))
        response = sock.recv(1024).decode('utf-8')
        print(f"Serwer mówi: {response}")

        if "gratulacje" in response.lower() or "odgadłeś" in response.lower():
            break

finally:
    sock.close()