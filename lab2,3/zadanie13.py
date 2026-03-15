import socket

src = 60788
dst = 2901

hex_data = "70 72 6f 67 72 61 6d 6d 69 6e 67 20 69 6e 20 70 79 74 68 6f 6e 20 69 73 20 66 75 6e"
bytes_data = bytes.fromhex(hex_data.replace(" ", ""))
decoded = bytes_data.decode('ascii')
message = f"zad14odp;src;{src};dst;{dst};data;{decoded}"
print(f"Wiadomość: {message}")

server_address = ('127.0.0.1', 2910)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)

try:
    sock.sendto(message.encode('utf-8'), server_address)
    a, _ = sock.recvfrom(1024)
    print(f"Odpowiedź: {a.decode('utf-8')}")
except socket.timeout:
    print("Błąd - timeout.")
finally:
    sock.close()

# Wyniki:
# Wiadomość: zad14odp;src;60788;dst;2901;data;programming in python is fun
# Odpowiedź: TAK
# Serwer:
# [2026-03-15 22:11:29] Lokalny tester UDP gotowy na porcie 2910...
# [2026-03-15 22:12:20] Odebrano od ('127.0.0.1', 59992): zad14odp;src;60788;dst;2901;data;programming in python is fun
# [2026-03-15 22:12:20] Wysłano odpowiedź: TAK

