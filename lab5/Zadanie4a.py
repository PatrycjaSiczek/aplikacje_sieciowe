import socket
import time

IP = "127.0.0.1"
PORT_TCP = 5001
PORT_UDP = 5002
NUM_PACKETS = 10000
MESSAGE = b"TestData"


def test_tcp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((IP, PORT_TCP))

    start_time = time.perf_counter()
    for _ in range(NUM_PACKETS):
        sock.send(MESSAGE)
    sock.send(b"END")
    end_time = time.perf_counter()

    sock.close()
    return end_time - start_time


def test_udp():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    start_time = time.perf_counter()
    for _ in range(NUM_PACKETS):
        sock.sendto(MESSAGE, (IP, PORT_UDP))
    sock.sendto(b"END", (IP, PORT_UDP))
    end_time = time.perf_counter()

    sock.close()
    return end_time - start_time


if __name__ == "__main__":
    print(f"Rozpoczynanie testu dla {NUM_PACKETS} pakietów...")

    time_tcp = test_tcp()
    print(f"Czas TCP: {time_tcp:.4f} sekundy")
    time.sleep(1)
    time_udp = test_udp()
    print(f"Czas UDP: {time_udp:.4f} sekundy")

    diff = abs(time_tcp - time_udp)
    faster = "UDP" if time_udp < time_tcp else "TCP"
    print(f"\nWynik: {faster} jest szybszy o {diff:.4f} sekundy.")