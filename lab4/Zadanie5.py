import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 2905))

while True:
    data, addr = s.recvfrom(1024)
    try:
        name = socket.gethostbyaddr(data.decode())[0]
        s.sendto(name.encode(), addr)
    except:
        s.sendto(b"Error", addr)