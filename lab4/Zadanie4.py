import socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 2904))

while True:
    data, addr = s.recvfrom(1024)
    try:
        parts = data.decode().split()
        v1, op, v2 = float(parts[0]), parts[1], float(parts[2])
        if op == '+': res = v1 + v2
        elif op == '-': res = v1 - v2
        elif op == '*': res = v1 * v2
        elif op == '/': res = v1 / v2 if v2 != 0 else "Error"
        s.sendto(str(res).encode(), addr)
    except:
        s.sendto(b"Error", addr)