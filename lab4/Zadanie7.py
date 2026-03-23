import socket

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 2907))
s.listen(1)

while True:
    c, addr = s.accept()
    buf = b""
    while len(buf) < 20:
        chunk = c.recv(20 - len(buf))
        if not chunk: break
        buf += chunk
    if len(buf) == 20:
        c.sendall(buf)
    c.close()