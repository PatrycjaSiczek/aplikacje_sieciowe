import socket

HOST = '127.0.0.1'
PORT = 1143

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Serwer oczekuje na polaczenie na {HOST}:{PORT}")

conn, addr = server_socket.accept()
print(f"\nPolaczono z klientem: {addr}")

conn.send(b"* OK IMAP4rev1 Service Ready\r\n")

file_in = conn.makefile('r', encoding='utf-8')

for line in file_in:
    tekst = line.strip()
    if not tekst:
        continue

    print(f"Klient wyslal: {tekst}")

    czesci = tekst.split(' ', 1)
    if len(czesci) < 2:
        print("Nieprawidlowy format komendy. Zwracam BAD.")
        conn.send(b"* BAD Invalid command format\r\n")
        continue

    tag = czesci[0]
    reszta_komendy = czesci[1].upper()

    if reszta_komendy.startswith("LOGIN"):
        print("Autoryzacja przebiegla pomyslnie.")
        conn.send(f"{tag} OK LOGIN completed\r\n".encode())

    elif reszta_komendy.startswith("LIST"):
        print("Wysylam liste skrzynek")
        conn.send(b"* LIST (\\HasNoChildren) \"/\" \"INBOX\"\r\n")
        conn.send(b"* LIST (\\HasNoChildren) \"/\" \"Sent\"\r\n")
        conn.send(f"{tag} OK LIST completed\r\n".encode())

    elif reszta_komendy.startswith("STATUS"):
        if "INBOX" in reszta_komendy:
            print("Wysylam status skrzynki INBOX")
            conn.send(b"* STATUS INBOX (MESSAGES 5)\r\n")
        else:
            print("Wysylam status innej skrzynki")
            conn.send(b"* STATUS \"Sent\" (MESSAGES 2)\r\n")
        conn.send(f"{tag} OK STATUS completed\r\n".encode())

    elif reszta_komendy.startswith("SELECT"):
        print("Otwieram skrzynke")
        conn.send(b"* 5 EXISTS\r\n")
        conn.send(b"* 1 RECENT\r\n")
        conn.send(f"{tag} OK [READ-WRITE] SELECT completed\r\n".encode())

    elif reszta_komendy.startswith("SEARCH"):
        print("Wiadomosci spelniajace kryteria")
        if "UNSEEN" in reszta_komendy:
            conn.send(b"* SEARCH 2 4\r\n")
        else:
            conn.send(b"* SEARCH 1 2 3 4 5\r\n")
        conn.send(f"{tag} OK SEARCH completed\r\n".encode())

    elif reszta_komendy.startswith("FETCH"):
        numer = reszta_komendy.split()[1]
        print(f"Wysylam tresc wiadomosci nr {numer}...")
        conn.send(
            f"* {numer} FETCH (BODY[] {{50}}\r\nTo jest tresc wiadomosci IMAP z testowego serwera.\r\n)\r\n".encode())
        conn.send(f"{tag} OK FETCH completed\r\n".encode())

    elif reszta_komendy.startswith("STORE"):
        numer = reszta_komendy.split()[1]
        print(f"Zmieniam flagi dla wiadomosci nr {numer}")
        conn.send(f"* {numer} FETCH (FLAGS (\\Seen \\Deleted))\r\n".encode())
        conn.send(f"{tag} OK STORE completed\r\n".encode())

    elif reszta_komendy.startswith("EXPUNGE"):
        print("Trwale usuwam wiadomosci z flaga \\Deleted")
        conn.send(f"{tag} OK EXPUNGE completed\r\n".encode())

    elif reszta_komendy.startswith("LOGOUT"):
        print("Rozlaczanie")
        conn.send(b"* BYE IMAP4rev1 Server logging out\r\n")
        conn.send(f"{tag} OK LOGOUT completed\r\n".encode())
        break

    else:
        print("Wysylam odpowiedz BAD.")
        conn.send(f"{tag} BAD Unknown command\r\n".encode())

conn.close()
server_socket.close()
print("Serwer IMAP zakonczyl prace.")