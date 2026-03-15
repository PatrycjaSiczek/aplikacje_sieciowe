import socket

server_address = ('127.0.0.1', 2908)
length = 20
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.settimeout(5)

try:
    sock.connect(server_address)
    user_input = input("Wpisz tekst: ")
    form = user_input.ljust(length)[:length]

    print(f"Do serwera: '{form}'")
    sock.sendall(form.encode('utf-8'))
    data = sock.recv(length)
    print(f"Odebrano: '{data.decode('utf-8')}'")

except Exception as e:
    print(f"Błąd")
finally:
    sock.close()

# Wyniki:
# Wpisz tekst: abcd
# Do serwera: 'abcd                '
# Odebrano: 'abcd
# Serwer
# [2026-03-09 15:38:09] TCP Fixed-Length (20 chars) Server is waiting...
# [2026-03-09 15:38:33] Client ('127.0.0.1', 51310) connected.
# [2026-03-09 15:38:38] Client ('127.0.0.1', 51310) sent: 'abcd                '
# [2026-03-09 15:38:38] Sending echo back...
# [2026-03-09 15:38:38] Client ('127.0.0.1', 51310) disconnected.