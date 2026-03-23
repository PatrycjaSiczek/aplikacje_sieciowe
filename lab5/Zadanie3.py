import socket

TARGET_IP = "212.182.24.27"
HIDDEN_TCP_PORT = 2913


def find_udp_sequence():
    knocking_sequence = []
    print("Szukanie portów UDP")

    for port in range(666, 65536, 1000):
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
            udp_sock.settimeout(0.5)
            try:
                udp_sock.sendto(b"PING", (TARGET_IP, port))
                data, _ = udp_sock.recvfrom(1024)
                if data.decode('utf-8') == "PONG":
                    print(f"port: {port}")
                    knocking_sequence.append(port)
            except socket.timeout:
                continue
    return knocking_sequence


def connect_to_hidden_service():
    sequence = find_udp_sequence()
    if not sequence:
        print("Nie znaleziono żadnych portów UDP.")
        return

    print("Wykonywanie port knocking...")
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as udp_sock:
        for port in sequence:
            udp_sock.sendto(b"PING", (TARGET_IP, port))

    print(f"Próba połączenia z ukrytą usługą na porcie TCP {HIDDEN_TCP_PORT}...")
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tcp_sock:
            tcp_sock.settimeout(5)
            tcp_sock.connect((TARGET_IP, HIDDEN_TCP_PORT))
            response = tcp_sock.recv(1024).decode('utf-8')
            print(f"Wiadomość z ukrytego portu: {response}")
    except Exception as e:
        print(f"Błąd połączenia TCP: {e}")


if __name__ == "__main__":
    connect_to_hidden_service()