import socket
import base64

sender = input("Podaj adres nadawcy : ")
password = input("Podaj haslo: ")
receiver = input("Podaj adres odbiorcy: ")
subject = input("Podaj temat wiadomosci: ")
body = input("Wpisz tresc wiadomosci: ")

login_b64 = base64.b64encode(sender.encode()).decode()
pass_b64 = base64.b64encode(password.encode()).decode()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(('interia.pl', 587))
sock.connect(('127.0.0.1', 2525))
print(f"Odebrano : {sock.recv(1024).decode().strip()}")
print("EHLO localhost")
sock.send(b"EHLO localhost\r\n")
print(f"Serwer:\n{sock.recv(1024).decode().strip()}")

print("AUTH LOGIN")
sock.send(b"AUTH LOGIN\r\n")
print(f"Serwer: {sock.recv(1024).decode().strip()}")

print("login")
sock.send(f"{login_b64}\r\n".encode())
print(f"Serwer: {sock.recv(1024).decode().strip()}")

print("haslo")
sock.send(f"{pass_b64}\r\n".encode())
print(f"Serwer: {sock.recv(1024).decode().strip()}")

print(f"Wysylanie komendy MAIL FROM:<{sender}>")
sock.send(f"MAIL FROM:<{sender}>\r\n".encode())
print(f"Serwer: {sock.recv(1024).decode().strip()}")

for rcpt in receiver.split(','):
    rcpt_clean = rcpt.strip()
    print(f"Wysylanie komendy RCPT TO:<{rcpt_clean}>")
    sock.send(f"RCPT TO:<{rcpt_clean}>\r\n".encode())
    print(f"Serwer: {sock.recv(1024).decode().strip()}")

print("Wysylanie komendy DATA")
sock.send(b"DATA\r\n")
print(f"Serwer: {sock.recv(1024).decode().strip()}")

msg = f"From: {sender}\r\nTo: {receiver}\r\nSubject: {subject}\r\n\r\n{body}\r\n.\r\n"
sock.send(msg.encode())
print(f"Serwer: {sock.recv(1024).decode().strip()}")

print("Wysylanie komendy QUIT")
sock.send(b"QUIT\r\n")
print(f"Serwer: {sock.recv(1024).decode().strip()}")

sock.close()
print("Koniec pracy programu")


# Wyniki
# Podaj adres nadawcy: pas2017@interia.pl
# Podaj haslo:  P4SInf2017
# Podaj adres odbiorcy: pas
# Podaj temat wiadomosci: test zadania 10 i 6
# Wpisz tresc wiadomosci: test abc

# Odebrano 220 localhost ESMTP FakeServer
# EHLO localhost
# Serwer:
# 250-localhost
# 250-AUTH LOGIN
# 250 OK
# AUTH LOGIN
# Serwer: 334 VXNlcm5hbWU6
# login
# Serwer: 334 UGFzc3dvcmQ6
# haslo
# Serwer: 235 2.7.0 Authentication successful
# Wysylanie komendy MAIL FROM:<pas2017@interia.pl>
# Serwer: 250 2.1.0 Ok
# Wysylanie komendy RCPT TO:<pas>
# Serwer: 250 2.1.5 Ok
# Wysylanie komendy DATA
# Serwer: 354 End data with <CR><LF>.<CR><LF>
# Serwer: 250 2.0.0 Ok: queued
# Wysylanie komendy QUIT
# Serwer: 221 2.0.0 Bye
# Koniec pracy programu
#
# Process finished with exit code 0