import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 2910))

while True:
    data, addr = s.recvfrom(1024)
    parts = data.decode().split(';')
    if len(parts) == 7 and parts[0] == "zad13odp" and parts[1] == "src" and parts[3] == "dst" and parts[5] == "data":
        if parts[2] == "2900" and parts[4] == "35211" and parts[6] == "hello :)":
            s.sendto(b"TAK", addr)
        else:
            s.sendto(b"NIE", addr)
    else:
        s.sendto(b"BAD SYNTAX", addr)