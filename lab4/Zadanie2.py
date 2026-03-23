import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 2902))
s.listen(1)

while True:
    c, addr = s.accept()
    data = c.recv(4096)
    if data:
        c.send(data)
    c.close()

# Wynik:
# Hello Echo TCP