import socket

HOST = '127.0.0.1'
PORT = 2525

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print("Serwer lokalny")
print(f"Serwer nasluchuje na {HOST}:{PORT}")

conn, addr = server_socket.accept()
print(f"\nUstanowiono polaczenie, adres klienta: {addr}")
conn.send(b"220 localhost ESMTP FakeServer\r\n")

file_in = conn.makefile('r', encoding='utf-8')

in_data_mode = False

for line in file_in:
    tekst = line.strip()
    if not tekst:
        continue

    print(f"Odebrano komende: {tekst}")
    command = tekst.upper()

    if in_data_mode:
        if tekst == ".":
            in_data_mode = False
            print("Wysylam: 250 2.0.0 Ok: queued")
            conn.send(b"250 2.0.0 Ok: queued\r\n")
        continue

    if command.startswith("HELO") or command.startswith("EHLO"):
        print("Wysylam: 250-localhost, 250-AUTH LOGIN, 250 OK")
        conn.send(b"250-localhost\r\n250-AUTH LOGIN\r\n250 OK\r\n")

    elif command.startswith("AUTH LOGIN"):
        print("Wysylam: 334 VXNlcm5hbWU6")
        conn.send(b"334 VXNlcm5hbWU6\r\n")

        login_data = file_in.readline().strip()
        print(f"Odebrano login: {login_data}")

        print("Wysylam: 334 UGFzc3dvcmQ6")
        conn.send(b"334 UGFzc3dvcmQ6\r\n")

        pass_data = file_in.readline().strip()
        print(f"Odebrano haslo: {pass_data}")

        print("Wysylam: 235 2.7.0 Authentication successful")
        conn.send(b"235 2.7.0 Authentication successful\r\n")

    elif command.startswith("MAIL FROM:"):
        print("Wysylam: 250 2.1.0 Ok")
        conn.send(b"250 2.1.0 Ok\r\n")

    elif command.startswith("RCPT TO:"):
        print("Wysylam: 250 2.1.5 Ok")
        conn.send(b"250 2.1.5 Ok\r\n")

    elif command == "DATA":
        in_data_mode = True
        print("Wysylam: 354 End data with <CR><LF>.<CR><LF>")
        conn.send(b"354 End data with <CR><LF>.<CR><LF>\r\n")

    elif command == "QUIT":
        print("Wysylam: 221 2.0.0 Bye")
        conn.send(b"221 2.0.0 Bye\r\n")
        break

    else:
        print("Nieznana komenda. Wysylam blad.")
        conn.send(b"502 5.5.2 Error: command not recognized\r\n")

conn.close()
server_socket.close()
print("Serwer wylaczyl sie.")

# Wyniki z zadaniem 6:
# Serwer nasluchuje na adresie 127.0.0.1 i porcie 2525
# Oczekuje na polaczenie od klienta...
#
# Ustanowiono polaczenie, adres klienta: ('127.0.0.1', 53880)
# Wysylam powitanie poczatkowe do klienta: 220 localhost ESMTP FakeServer
# Odebrano komende z zewnatrz: EHLO localhost
# Wysylam przedstawienie: 250-localhost, 250-AUTH LOGIN, 250 OK
# Odebrano komende z zewnatrz: AUTH LOGIN
# Wysylam zadanie loginu Base64: 334 VXNlcm5hbWU6
# Odebrano zakodowany login: cGFzMjAxN0BpbnRlcmlhLnBs
# Wysylam zadanie hasla Base64: 334 UGFzc3dvcmQ6
# Odebrano zakodowane haslo: IFA0U0luZjIwMTc=
# Wysylam sukces autoryzacji: 235 2.7.0 Authentication successful
# Odebrano komende z zewnatrz: MAIL FROM:<pas2017@interia.pl>
# Wysylam akceptacje nadawcy: 250 2.1.0 Ok
# Odebrano komende z zewnatrz: RCPT TO:<pas>
# Wysylam akceptacje odbiorcy: 250 2.1.5 Ok
# Odebrano komende z zewnatrz: DATA
# Wysylam zgode na tresc: 354 End data with <CR><LF>.<CR><LF>
# Odebrano komende z zewnatrz: From: pas2017@interia.pl
# To: pas
# Subject: test zadania 10 i 6
#
# test abc
# .
# Klient zakonczyl wiadomosc kropka. Wysylam: 250 2.0.0 Ok: queued
# Odebrano komende z zewnatrz: QUIT
# Wysylam komende wyjscia: 221 2.0.0 Bye
# Serwer wylaczyl sie poprawnie.
#
# Process finished with exit code 0

# Odpowiedz lokalnego serwera:
# Serwer lokalny
# Serwer nasluchuje na adresie 127.0.0.1 i porcie 2525
# Oczekuje na polaczenie od klienta...
#
# Ustanowiono polaczenie! Adres klienta: ('127.0.0.1', 51379)
# Wysylam powitanie poczatkowe do klienta: 220 localhost ESMTP FakeServer
# Odebrano komende z zewnatrz: EHLO localhost
# Wysylam przedstawienie: 250-localhost, 250-AUTH LOGIN, 250 OK
# Odebrano komende z zewnatrz: AUTH LOGIN
# Wysylam zadanie loginu Base64: 334 VXNlcm5hbWU6
# Odebrano zakodowany login: cGFzMjAxN0BnbWFpbC5jb3Bt
# Wysylam zadanie hasla Base64: 334 UGFzc3dvcmQ6
# Odebrano zakodowane haslo: YWJjZGU=
# Wysylam sukces autoryzacji: 235 2.7.0 Authentication successful
# Odebrano komende z zewnatrz: MAIL FROM:<pas2017@gmail.copm>
# Wysylam akceptacje nadawcy: 250 2.1.0 Ok
# Odebrano komende z zewnatrz: RCPT TO:<xyz>
# Wysylam akceptacje odbiorcy: 250 2.1.5 Ok
# Odebrano komende z zewnatrz: DATA
# Wysylam zgode na tresc: 354 End data with <CR><LF>.<CR><LF>
# Odebrano komende z zewnatrz: From: pas2017@gmail.copm
# To: xyz
# Subject: xyzz
# MIME-Version: 1.0
# Content-Type: multipart/mixed; boundary=BOUNDARY_SEP_123
#
# --BOUNDARY_SEP_123
# Content-Type: text/plain; charset=utf-8
#
# abcdd
#
# --BOUNDARY_SEP_123
# Content-Type: text/plain; name="testDo7.txt"
# Content-Disposition: attachment; filename="testDo7.txt"
# Content-Transfer-Encoding: base64
#
# dGVrc3QgZG8gemFkYW5pYSA3
# --BOUNDARY_SEP_123--
# .
# Klient zakonczyl wiadomosc kropka. Wysylam: 250 2.0.0 Ok: queued
# Odebrano komende z zewnatrz: QUIT
# Wysylam komende wyjscia: 221 2.0.0 Bye
# Serwer wylaczyl sie poprawnie.
#
# Process finished with exit code 0
