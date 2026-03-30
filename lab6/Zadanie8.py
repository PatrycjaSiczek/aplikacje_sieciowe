import socket
import base64
import os

sender = input("Podaj adres nadawcy: ")
password = input("Podaj haslo: ")
receiver = input("Podaj adres odbiorcy: ")
subject = input("Podaj temat wiadomosci: ")
body = input("Wpisz tresc wiadomosci: ")
image_path = input("Podaj sciezke do obrazka: ")

print(f"\nWczytywanie obrazka {image_path} i kodowanie do Base64...")
with open(image_path, 'rb') as f:
    img_data = base64.b64encode(f.read()).decode()

filename = os.path.basename(image_path)
login_b64 = base64.b64encode(sender.encode()).decode()
pass_b64 = base64.b64encode(password.encode()).decode()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# sock.connect(('interia.pl', 587))
sock.connect(('127.0.0.1', 2525))
sock.recv(1024)

print("Logowanie na serwer SMTP")
sock.send(b"EHLO localhost\r\n")
sock.recv(1024)
sock.send(b"AUTH LOGIN\r\n")
sock.recv(1024)
sock.send(f"{login_b64}\r\n".encode())
sock.recv(1024)
sock.send(f"{pass_b64}\r\n".encode())
sock.recv(1024)

print("Ustawianie nadawcy i odbiorcow")
sock.send(f"MAIL FROM:<{sender}>\r\n".encode())
sock.recv(1024)

for rcpt in receiver.split(','):
    sock.send(f"RCPT TO:<{rcpt.strip()}>\r\n".encode())
    sock.recv(1024)

print("Wysylanie obrazka jako Image/JPEG w strukturze MIME")
sock.send(b"DATA\r\n")
sock.recv(1024)

boundary = "IMG_BOUNDARY_456"
msg = f"From: {sender}\r\nTo: {receiver}\r\nSubject: {subject}\r\nMIME-Version: 1.0\r\nContent-Type: multipart/mixed; boundary={boundary}\r\n\r\n--{boundary}\r\nContent-Type: text/plain; charset=utf-8\r\n\r\n{body}\r\n\r\n--{boundary}\r\nContent-Type: image/jpeg; name=\"{filename}\"\r\nContent-Disposition: attachment; filename=\"{filename}\"\r\nContent-Transfer-Encoding: base64\r\n\r\n{img_data}\r\n--{boundary}--\r\n.\r\n"

sock.send(msg.encode())
print(f"Serwer : {sock.recv(1024).decode().strip()}")

sock.send(b"QUIT\r\n")
sock.recv(1024)
sock.close()
print("Udao sie wyslac obrazek.")

# Podaj adres nadawcy: pas2017@interia.pl
# Podaj haslo:  P4SInf2017
# Podaj adres odbiorcy: pasinf2017@interia.pl
# Podaj temat wiadomosci: zadanie8
# Wpisz tresc wiadomosci: tekst do 8
# Podaj sciezke do obrazka: lena.png
#
# Wczytywanie obrazka lena.png i kodowanie do Base64
# Logowanie na serwer SMTP
# Ustawianie nadawcy i odbiorcow...
# Wysylanie obrazka jako Image/JPEG w strukturze MIME
# Serwer: 250 2.0.0 Ok: queued
# Udalo sie wyslac obrazek
#
# Process finished with exit code 0


# Odpowiedz od serwera:
# Serwer nasluchuje na adresie 127.0.0.1 i porcie 2525
# Oczekuje na polaczenie od klienta...
# Ustanowiono polaczenie! Adres klienta: ('127.0.0.1', 53729)
# Wysylam powitanie poczatkowe do klienta: 220 localhost ESMTP FakeServer
# Odebrano komende z zewnatrz: EHLO localhost
# Wysylam przedstawienie: 250-localhost, 250-AUTH LOGIN, 250 OK
# Odebrano komende z zewnatrz: AUTH LOGIN
# Wysylam zadanie loginu Base64: 334 VXNlcm5hbWU6
# Odebrano zakodowany login: cGFzMjAxN0BpbnRlcmlhLnBsIA==
# Wysylam zadanie hasla Base64: 334 UGFzc3dvcmQ6
# Odebrano zakodowane haslo: IFA0U0luZjIwMTc=
# Wysylam sukces autoryzacji: 235 2.7.0 Authentication successful
# Odebrano komende z zewnatrz: MAIL FROM:<pas2017@interia.pl >
# Wysylam akceptacje nadawcy: 250 2.1.0 Ok
# Odebrano komende z zewnatrz: RCPT TO:<pasinf2017@interia.pl>
# Wysylam akceptacje odbiorcy: 250 2.1.5 Ok
# Odebrano komende z zewnatrz: DATA
# Wysylam zgode na tresc: 354 End data with <CR><LF>.<CR><LF>
# Odebrano komende z zewnatrz: From: pas2017@interia.pl
# To: pasinf2017@interia.pl
# Subject: zadanie8
# MIME-Version: 1.0
# Content-Type: multipart/mixed; boundary=IMG_BOUNDARY_456
#
# --IMG_BOUNDARY_456
# Content-Type: text/plain; charset=utf-8
#
# tekst do 8
#
# --IMG_BOUNDARY_456
# Content-Type: image/jpeg; name="lena.png"
# Content-Disposition: attachment; filename="lena.png"
# Content-Transfer-Encoding: base64
#
# iVBORw0KGgoAAAANSUhEUgAAAgAAAAIACAIAAAB7GkOtAAAACXBIWXMAAAp1AAAKdQFKJd39AAAAB3RJTUUH1wgXFxQ3sStlfwAAIABJREFUeNrs212ubUuSJeQxzMx9zrX2PufciMiiHuqFFiAhJBCIPyUvdAaVqOKVBtA4GkBRpRIJZJARGXF/zt5rreluZoOHm62A+3XC3IYN59/9L/8zgMIJbbcXnmm3Q0lM73y5jtLu/O63t0r2WhgLNXic4MWPjZGsqnFU0c2ttu1Hjn8OPdR3jw/L1cf0VXX8YP2wt3d7/qMdfwAvKpvDj2DDp6W6ExNNVC7jW+i5ugavZ/Wtfv6HZUcf/8H68a+Pj6WfPn6O4/vH2p+vMr46dh+2frL339/G3utzHIeyI4JUyIBk2Ti9bDNbMvRuAeds+OxqNdsEkBUWiUIVPQrDeUlHYmlvmo0u2qiogYm7+8eyMB8eQWTma9/e7olqb/OD9ch+v9mnaejukXzuHdUxRt09skWzXXaeay12097K2vYz334/7XsvN5L1KgxluqfGu33/nsfRtXg/mIvFdvN85vgb398b5udp+hD/gH7i9ZjH7J37vFldRIjmcOQDccb1ue9vlq1CO1zZY3LtFefQq3uL
# Odebrano komende z zewnatrz: t+6c2I07Ah3y7Yvtu3vId2sGadwvxQhs4Ib8yPMLK9GZ/SX8RcmIV7Fs2PnOx49R1W+/7/XBulqX2Vk4M3++mZXDIE+UGva1uJm772/qGnrA3nLnqVW4k092lb+N/R10kRXhFuhLDTfvvjpukHxYXq9Ztfwwjrq2ofq42RgkfDAfn9kGyPZrG9FvN180vVJwOzg3EPV4ypxY7XdvGfczeOAYtTFtrUdb6GnzsPXq8cXc+Pi+6XaeI1u5FUfnxqF8GqLNJq+ngq7M4wdeP77mV34+FU4dlk9UruNga6lLVGVXlyHM8vtjt5LH1/7wtzH5A8f3w2K+nyPaxjQNzXATj4J/i346q26HYRPNcWpdebxDT388obd+/mIMHeLldYob0drn8PXi/CHbvX7meKOubgek44v3k/lR/oX13ZpdG7cvWtlabmH6kN2rDvKTMBPUDUS+u18NpJTSdLt6fMXeOiaVreH7ahI8fHSDAJRheAih/T3jn9P/dOB2/osx/uYPcZrf3ujycRM3dWMYLUB4b1nBjtqr17Wvx+cv+/l/f/z8x/UP/+7PP/1Fja1V8IDlcRx49HiXW5ilm6PUdghpoZtina5Xzv35xJvHHjGQj9rDD0udGm1+6PmojojY+dNdFo5toVUacd+fD3+/6/p5nG998XjLX777ERXO8nYMXc23zHR7URHIx1XSeX619bIYoIpyzDPXj2b3ka/KxPtbrQx7FP7Qz597zv1R89Z1FeNsXtrU8f5mr29f71/+w38xRpuXW6X0/OvHn/+PfzT85je/+c1v/n/ptwHwm9/85je/DYDf/OY3v/nNbwPgN7/5zW9+8/95/q/++/+KJrt+rnqaDWN1MfAsfHq7rp8Vk/nRVxgepgUyJL1ezt252fKcvB4+7sRmlYZaP1h9cHzQvCP48hSVP8nfrR5Bbwc7NYb7gMysmj7MPItlusnqBv7F1kluPn/Z9N6qPvh4XD//uF6Z4PXsCqaGdlene6P3qVZ1UI5IO3Fp1LNu73N/1Ah2
# Odebrano komende z zewnatrz: 2koj5Y1Wbpi1Xarooy88Vw2fK1sqkwpay/zg+oxBvbLdpi0db3jtjtGBeC34gfsx1kUBDhthGKVlpLHU52iPiQbxvNpG0F3KdmV39mHZY2bFqCtvZ8mol/VlbIp7N3bjNq0S5uaonsiXwXuM6unhFCgflcIwE2g2Tm8HiEazGA67YbRp2KCbOT+Em+MJDBitL0wru436STqc22ZVj5Etghc5SzPw+RndQrHk2gPddne82LvMo0uN5q76Mq4f26X+hvGyfY1am0K9+ZQ/fw6yh7cXPj96ksu81NqjRFWNGZWugACjc/dW74vWoc7TcOXz2uU3U61m4AmEMpPM2xueDzJa1XGyd7dobo9HM3oc8boK5dyKE2brqmOtFiWnb9Zsq/B4VJ3OXi8Os+zar4IDdgxxZfM0lxWNKznKT1X08zNWAqKx5w9an6SXHdFbe9GPYEJV5w1PmSdVGie15eGVsbFpLImwfDW3MRhsZ+eqMqkdPWLW9ame2SWfYI2rMGLV+hpoH0ZXPXF8850+JpjmB5WoMp5Et27BN+kXG9+wNmuZD6wLdsprdOfRvt7JR45vvj5rJ+nmzeerg6RXLWOiXlzfNd6NmzLHBXPkC6Abkd1w9iRWoBVv2OzTPT+bNx+lOcTNIgyQ+97Ci7rDW9jgYIy+lrWIyxBCoxIK5QM9O+4+HnYMZ5CX+VcQMHcrwCjQijKhm2VuwAQKImzx2bvx+P5Rr91ZHqdnWj9x/53pudTjeKtcgy7tWz8BJ/NYjzoP1yp/Z360z6nVx13qDvci8yrL6XzlBqMTfZiv1+4Il/WLPjglm2gCa1rRj95ZvXvMsK7aQvkx1C/1UUrHxriN/NTujHF6tnKQtmWxzSmbhY0y1y5gUC7rVewdx7tcI8wOM+M5YI+/vJZ//vLXn//h88//9o//+//24//6b9L/9X/7X7C6b2AbcHq8rIF8wiZ8oGCTVp/yNkJbVGn+jfTwDR5vvT4tDqLTjAJL9PLrVY02t+NGGUS3l3Gan7NfOiwQ
# ...
# --IMG_BOUNDARY_456--
# .
# Klient zakonczyl wiadomosc kropka. Wysylam: 250 2.0.0 Ok: queued
# Odebrano komende z zewnatrz: QUIT
# Wysylam komende wyjscia: 221 2.0.0 Bye
# Serwer wylaczyl sie poprawnie.
