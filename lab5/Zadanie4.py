import socket

IP = "127.0.0.1"
PORT_TCP = 5001
PORT_UDP = 5002
BUFFER_SIZE = 1024


def start_server():

    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.bind((IP, PORT_TCP))
    tcp_sock.listen(1)
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind((IP, PORT_UDP))

    print("Serwer testowy gotowy. Czekam na dane...")

    conn, addr = tcp_sock.accept()
    while True:
        data = conn.recv(BUFFER_SIZE)
        if not data or b"END" in data: break
    conn.close()
    print("Zakończono test TCP.")

    while True:
        data, addr = udp_sock.recvfrom(BUFFER_SIZE)
        if b"END" in data: break
    print("Zakończono test UDP.")

    tcp_sock.close()
    udp_sock.close()


if __name__ == "__main__":
    start_server()