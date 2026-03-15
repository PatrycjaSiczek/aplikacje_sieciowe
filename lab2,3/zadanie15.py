import socket

server = ('127.0.0.1', 2911)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.settimeout(5)

ver = 4
srcIp = "192.168.0.2"
dstIp = "11.84.185.166"
p = 6
srcPort = 64505
dstPort = 15447
data_text = "programming in python is fun"

try:
    msgA = f"zad15odpA;ver;{ver};src;{srcIp};dst;{dstIp};type;{p}"
    print(f"A: {msgA}")
    sock.sendto(msgA.encode('utf-8'), server)
    a, _ = sock.recvfrom(1024)
    print(f"Serwer A: {a.decode('utf-8')}")

    if a.decode('utf-8') == "TAK":
        msgB = f"zad15odpB;srcport;{srcPort};dstport;{dstPort};data;{data_text}"
        print(f"B: {msgB}")
        sock.sendto(msgB.encode('utf-8'), server)

        b, _ = sock.recvfrom(1024)
        print(f"Serwer B: {b.decode('utf-8')}")

except socket.timeout:
    print("Blad: timeout")
except Exception as e:
    print(f"Blad: {e}")
finally:
    sock.close()

# Wyniki:
# A: zad15odpA;ver;4;src;192.168.0.2;dst;11.84.185.166;type;6
# Serwer A: TAK
# B: zad15odpB;srcport;64505;dstport;15447;data;programming in python is fun
# Serwer B: TAK
# Serwer:
# [2026-03-15 22:42:54] Odebrano od ('127.0.0.1', 59009): zad15odpA;ver;4;src;192.168.0.2;dst;11.84.185.166;type;6
# [2026-03-15 22:42:54] Wysłano odpowiedź: TAK
# [2026-03-15 22:42:54] Odebrano od ('127.0.0.1', 59009): zad15odpB;srcport;64505;dstport;15447;data;programming in python is fun
# [2026-03-15 22:42:54] Wysłano odpowiedź: TAK