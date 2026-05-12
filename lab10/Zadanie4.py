import socket
import base64
import hashlib

HOST = '127.0.0.1'
PORT = 8081

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Oczekuje na polaczenia na porcie {PORT}...")

while True:
    conn, addr = server_socket.accept()
    print(f"\nPolaczono z uzytkownikiem pod adresem {addr}")

    dane_powitalne = conn.recv(4096).decode('utf-8', errors='ignore')

    klucz_klienta = ""
    for linia in dane_powitalne.split('\r\n'):
        if linia.lower().startswith("sec-websocket-key:"):
            klucz_klienta = linia.split(":")[1].strip()

    if klucz_klienta:
        print(f"Zlapano klucz od klienta: {klucz_klienta}")
        magiczny_guid = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
        ciag_do_shashowania = klucz_klienta + magiczny_guid

        hash_sha1 = hashlib.sha1(ciag_do_shashowania.encode('utf-8')).digest()
        klucz_potwierdzajacy = base64.b64encode(hash_sha1).decode('utf-8')

        odpowiedz = "HTTP/1.1 101 Switching Protocols\r\n"
        odpowiedz += "Upgrade: websocket\r\n"
        odpowiedz += "Connection: Upgrade\r\n"
        odpowiedz += f"Sec-WebSocket-Accept: {klucz_potwierdzajacy}\r\n\r\n"

        print("Zatwierdzam autoryzacje i przelaczam na WebSocket")
        conn.send(odpowiedz.encode('utf-8'))

        print("Czekam na ramke z danymi od klienta")
        ramka_od_klienta = conn.recv(4096)

        if len(ramka_od_klienta) >= 6:
            dlugosc_payloadu = ramka_od_klienta[1] & 127
            klucz_maskujacy = ramka_od_klienta[2:6]
            dane_zamaskowane = ramka_od_klienta[6:6 + dlugosc_payloadu]

            dane_odkodowane = bytearray()
            for i in range(dlugosc_payloadu):
                odmaskowany_bajt = dane_zamaskowane[i] ^ klucz_maskujacy[i % 4]
                dane_odkodowane.append(odmaskowany_bajt)

            tekst = dane_odkodowane.decode('utf-8', errors='ignore')
            print(f"Pomyslnie rozszyfrowano ramke! Wiadomosc to: {tekst}")

            print("Odsylam potwierdzenie")
            odpowiedz_serwera = bytearray()
            odpowiedz_serwera.append(0x81)
            odpowiedz_serwera.append(len(tekst))
            odpowiedz_serwera.extend(tekst.encode('utf-8'))
            conn.send(odpowiedz_serwera)

    conn.close()
    print("Polaczenie przerwane przez serwer.")

    # Wyniki z zadaiem 3
    # Oczekuje na polaczenia na porcie 8081
    # Polaczono z uzytkownikiem pod adresem('127.0.0.1', 56360)
    # Zlapano klucz od klienta: twTMllprYjBaW4ttry11gg ==
    # Zatwierdzam autoryzacje i przelaczam na WebSocket.
    # Czekam na ramke z danymi od klienta.
    # Pomyslnie rozszyfrowano ramke!
    # Wiadomosc to: AAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAKAAK
    # Odsylam potwierdzenie
    # Polaczenie przerwane przez serwer.