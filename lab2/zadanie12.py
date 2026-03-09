import socket

server_address = ('127.0.0.1', 2908)
length = 20

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(10)

try:
    sock.connect(server_address)
    message = input("Wpisz wiadomość: ")
    form = message.ljust(length)[:length]
    print(f"Wysyłano: '{form}'")
    sock.sendall(form.encode('utf-8'))
    received= b""

    while len(received) < length:
        to_receive = length - len(received)
        chunk = sock.recv(to_receive)
        if not chunk:
            print("Połączenie przerwane")
            break
        received += chunk
        print(f"Odebrano fragment ({len(received)}/20 bajtów)")
    print(f"Pełna odebrana wiadomość: [{received.decode('utf-8')}]")

except Exception as e:
    print(f"Błąd")
finally:
    sock.close()
    print("Zamknięto")

# Wyniki:
# Wpisz wiadomość: xyz
# Wysyłano: 'xyz                 '
# Odebrano fragment (20/20 bajtów)
# Pełna odebrana wiadomość: [xyz                 ]
# Zamknięto
# Serwer:
# [2026-03-09 15:40:37] TCP ECHO Server (20 bytes) is waiting on port 2908...
# [2026-03-09 15:46:37] Client ('127.0.0.1', 55999) connected.
# [2026-03-09 15:46:49] Client ('127.0.0.1', 55999) sent: 'xyz                 '
# [2026-03-09 15:46:49] Sending back to client...
# [2026-03-09 15:46:49] Client ('127.0.0.1', 55999) disconnected.