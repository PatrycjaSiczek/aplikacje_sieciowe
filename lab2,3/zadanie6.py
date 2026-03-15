import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)

server = ('127.0.0.1', 2902)
x = input("Podaj liczbe: ")
y = input("Podaj operator: ")
z = input("Podaj druga liczbe ")

message = f"{x} {y} {z}"

try:
    sock.sendto(message.encode('utf-8'), server)
    data, _ = sock.recvfrom(1024)
    print(f"Odpowiedz serwera: {data.decode('utf-8')}")
except socket.error as exc:
    print("Wyjatek socket.error : %s" % exc)
finally:
    print("Zamkniecie")
    sock.close()

# Wyniki:
# Podaj liczbe: 5
# Podaj operator: +
# Podaj druga liczbe 2
# Odpowiedz serwera: 7.0
# Zamkniecie
# Serwer:
# [2026-03-09 12:34:56] UDP Calc Server czeka na dane na porcie 2902...
# [2026-03-09 12:35:13] Otrzymano od ('127.0.0.1', 62283): 5 + 2
# Sent result: 7.0 to ('127.0.0.1', 62283)


