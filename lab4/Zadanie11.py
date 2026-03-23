import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 2911))

while True:
    data, addr = s.recvfrom(1024)
    txt = data.decode()
    parts = txt.split(';')
    if parts[0] == "zad15odpA":
        if len(parts) == 9 and parts[2] == "4" and parts[4] == "192.168.0.2" and parts[6] == "11.84.185.166" and parts[8] == "6":
            s.sendto(b"TAK", addr)
        else: s.sendto(b"NIE", addr)
    elif parts[0] == "zad15odpB":
        if len(parts) == 7 and parts[2] == "64505" and parts[4] == "15447" and parts[6] == "programming in python is fun":
            s.sendto(b"TAK", addr)
        else: s.sendto(b"NIE", addr)
    else:
        s.sendto(b"BAD SYNTAX", addr)