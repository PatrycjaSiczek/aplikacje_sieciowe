import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 2906))

while True:
    data, addr = s.recvfrom(1024)
    try:
        ip = socket.gethostbyname(data.decode())
        s.sendto(ip.encode(), addr)
    except:
        s.sendto(b"Error", addr)