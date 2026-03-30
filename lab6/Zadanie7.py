import socket
import base64
import os


sender = input("Podaj adres nadawcy: ")
password = input("Podaj haslo: ")
receiver = input("Podaj adres odbiorcy: ")
subject = input("Podaj temat wiadomosci: ")
body = input("Wpisz tresc wiadomosci: ")
filepath = input("Podaj sciezke do pliku tekstowego: ")

with open(filepath, 'rb') as f:
    file_data = base64.b64encode(f.read()).decode()

filename = os.path.basename(filepath)
login_b64 = base64.b64encode(sender.encode()).decode()
pass_b64 = base64.b64encode(password.encode()).decode()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(('interia.pl', 587))
sock.connect(('127.0.0.1', 2525))
sock.recv(1024)

print("Rozpoczecie autoryzacji")
sock.send(b"EHLO localhost\r\n")
sock.recv(1024)
sock.send(b"AUTH LOGIN\r\n")
sock.recv(1024)
sock.send(f"{login_b64}\r\n".encode())
sock.recv(1024)
sock.send(f"{pass_b64}\r\n".encode())
sock.recv(1024)

print("Przesylanie adresow nadawcy i odbiorcy")
sock.send(f"MAIL FROM:<{sender}>\r\n".encode())
sock.recv(1024)

for rcpt in receiver.split(','):
    sock.send(f"RCPT TO:<{rcpt.strip()}>\r\n".encode())
    sock.recv(1024)

print("Wysylanie struktury MIME wraz z zalacznikiem")
sock.send(b"DATA\r\n")
sock.recv(1024)

boundary = "BOUNDARY_SEP_123"
msg = f"From: {sender}\r\nTo: {receiver}\r\nSubject: {subject}\r\nMIME-Version: 1.0\r\nContent-Type: multipart/mixed; boundary={boundary}\r\n\r\n--{boundary}\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n{body}\r\n\r\n--{boundary}\r\nContent-Type: text/plain; name=\"{filename}\"\r\nContent-Disposition: attachment; filename=\"{filename}\"\r\nContent-Transfer-Encoding: base64\r\n\r\n{file_data}\r\n--{boundary}--\r\n.\r\n"

sock.send(msg.encode())
print(f"Odpowiedz serwera po wyslaniu: {sock.recv(1024).decode().strip()}")

sock.send(b"QUIT\r\n")
sock.recv(1024)
sock.close()
print("Wiadomosc z zalacznikiem wyslana.")


# Wyniki:
# Podaj adres nadawcy: pas2017@gmail.copm
# Podaj haslo: abcde
# Podaj adres odbiorcy: xyz
# Podaj temat wiadomosci: xyzz
# Wpisz tresc wiadomosci: abcdd
# Podaj sciezke do pliku tekstowego: testDo7.txt

# Rozpoczecie autoryzacji
# Przesylanie adresow nadawcy i odbiorcy
# Wysylanie struktury MIME wraz z zalacznikiem
# Odpowiedz serwera po wyslaniu: 250 2.0.0 Ok: queued
# Wiadomosc z zalacznikiem wyslana.
# Process finished with exit code 0

