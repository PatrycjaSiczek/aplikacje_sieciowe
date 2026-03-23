import socket
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('127.0.0.1', 2901))
s.listen(1)

while True:
    c, addr = s.accept()
    data = c.recv(1024)
    if data:
        now = time.strftime("%Y-%m-%d %H:%M:%S")
        c.send(now.encode())
    c.close()

# Wyniki:
# 2026-03-16 11:42:06