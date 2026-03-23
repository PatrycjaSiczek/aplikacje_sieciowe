import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 2909))

while True:
    data, addr = s.recvfrom(1024)
    parts = data.decode().split(';')
    if len(parts) == 7 and parts[0] == "zad14odp" and parts[1] == "src" and parts[3] == "dst" and parts[5] == "data":
        if parts[2] == "60788" and parts[4] == "2901" and parts[6] == "programming in python is fun":
            s.sendto(b"TAK", addr)
        else:
            s.sendto(b"NIE", addr)
    else:
        s.sendto(b"BAD SYNTAX", addr)