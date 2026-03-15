import socket

server = ('127.0.0.1', 2909)
src = 2900
dst = 35211
hex = "68656c6c6f203a29"
decoded = bytes.fromhex(hex).decode('ascii')

message = f"zad13odp;src;{src};dst;{dst};data;{decoded}"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)

try:
    sock.sendto(message.encode('utf-8'), server)
    a, _ = sock.recvfrom(1024)
    print(a.decode('utf-8'))
except socket.timeout:
    print("Błąd: timeout")
finally:
    sock.close()

# Wyniki:
# TAK
# Serwer:
# Serwer testowy działa... Czekam na klienta.
# Otrzymano: zad13odp;src;2900;dst;35211;data;hello :)
