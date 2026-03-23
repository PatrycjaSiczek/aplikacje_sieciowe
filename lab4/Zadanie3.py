import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 2903))

while True:
    data, addr = s.recvfrom(4096)
    s.sendto(data, addr)