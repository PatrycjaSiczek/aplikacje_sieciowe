import socket
import base64

sender = input("Podaj adres nadawcy: ")
password = input("Podaj haslo: ")
receiver = input("Podaj adres odbiorcy: ")
subject = input("Podaj temat wiadomosci: ")

html_body = "<html><body><b>To jest pogrubienie</b>, <i>pochylenie</i> i <u>podkreslenie</u>.</body></html>"

login_b64 = base64.b64encode(sender.encode()).decode()
pass_b64 = base64.b64encode(password.encode()).decode()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(('poczta.interia.pl', 587))
sock.connect(('127.0.0.1', 2525))
sock.recv(1024)

print("Autoryzacja serwera...")
sock.send(b"EHLO localhost\r\n")
sock.recv(1024)
sock.send(b"AUTH LOGIN\r\n")
sock.recv(1024)
sock.send(f"{login_b64}\r\n".encode())
sock.recv(1024)
sock.send(f"{pass_b64}\r\n".encode())
sock.recv(1024)

sock.send(f"MAIL FROM:<{sender}>\r\n".encode())
sock.recv(1024)

for rcpt in receiver.split(','):
    sock.send(f"RCPT TO:<{rcpt.strip()}>\r\n".encode())
    sock.recv(1024)

print("Wysylanie tresci o typie Content-Type: text/html")
sock.send(b"DATA\r\n")
sock.recv(1024)

msg = f"From: {sender}\r\nTo: {receiver}\r\nSubject: {subject}\r\nMIME-Version: 1.0\r\nContent-Type: text/html; charset=utf-8\r\n\r\n{html_body}\r\n.\r\n"
sock.send(msg.encode())
print(f"Status wysylania: {sock.recv(1024).decode().strip()}")

sock.send(b"QUIT\r\n")
sock.recv(1024)
sock.close()
print("Wyslano wiadomosc sformatowana w HTML.")

#Wyniki:
# Podaj adres nadawcy:  pas2017@interia.plP4SInf2017
# Podaj haslo: P4SInf2017
# Podaj adres odbiorcy: pasinf2017@interia.pl
# Podaj temat wiadomosci: zadanie9

# Autoryzacja serwera...
# Wysylanie tresci o typie Content-Type: text/html...
# Status wysylania: 250 2.0.0 Ok: queued
# Wyslano wiadomosc sformatowana w HTML.
#
# Odpowiedz serwera:
# "C:\Users\patry\OneDrive\Pulpit\Semestr6\Aplikacje Sieciowe\lab1\Scripts\python.exe" C:\Users\patry\PycharmProjects\aplikacje_sieciowe\lab6\Zadanie10.py
# --- Uruchomiono lokalny serwer testowy ---
# Serwer nasluchuje na adresie 127.0.0.1 i porcie 2525
# Oczekuje na polaczenie od klienta...
#
# Ustanowiono polaczenie! Adres klienta: ('127.0.0.1', 61369)
# Wysylam powitanie poczatkowe do klienta: 220 localhost ESMTP FakeServer
# Odebrano komende z zewnatrz: EHLO localhost
# Wysylam przedstawienie: 250-localhost, 250-AUTH LOGIN, 250 OK
# Odebrano komende z zewnatrz: AUTH LOGIN
# Wysylam zadanie loginu Base64: 334 VXNlcm5hbWU6
# Odebrano zakodowany login: IHBhczIwMTdAaW50ZXJpYS5wbA==
# Wysylam zadanie hasla Base64: 334 UGFzc3dvcmQ6
# Odebrano zakodowane haslo: UDRTSW5mMjAxNw==
# Wysylam sukces autoryzacji: 235 2.7.0 Authentication successful
# Odebrano komende z zewnatrz: MAIL FROM:< pas2017@interia.pl>
# Wysylam akceptacje nadawcy: 250 2.1.0 Ok
# Odebrano komende z zewnatrz: RCPT TO:<pasinf2017@interia.pl>
# Wysylam akceptacje odbiorcy: 250 2.1.5 Ok
# Odebrano komende z zewnatrz: DATA
# Wysylam zgode na tresc: 354 End data with <CR><LF>.<CR><LF>
# Odebrano komende z zewnatrz: From:  pas2017@interia.pl
# To: pasinf2017@interia.pl
# Subject: zadanie9
# MIME-Version: 1.0
# Content-Type: text/html; charset=utf-8
#
# <html><body><b>To jest pogrubienie</b>, <i>pochylenie</i> i <u>podkreslenie</u>.</body></html>
# .
# Klient zakonczyl wiadomosc kropka. Wysylam: 250 2.0.0 Ok: queued
# Odebrano komende z zewnatrz: QUIT
# Wysylam komende wyjscia: 221 2.0.0 Bye
# Serwer wylaczyl sie poprawnie.
#
# Process finished with exit code 0
