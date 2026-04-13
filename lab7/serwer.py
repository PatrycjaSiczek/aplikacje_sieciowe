import socket

HOST = '127.0.0.1'
PORT = 1110

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

skrzynka_pocztowa = {}

for i in range(1, 18):
    skrzynka_pocztowa[
        i] = f"+OK 100 octets\r\nFrom: nadawca{i}@serwer.pl\r\nTo: pasinf2017@interia.pl\r\nSubject: Wygenerowana wiadomosc {i}\r\n\r\nTo jest automatyczna tresc wiadomosci numer {i}.\r\nSystem dziala w pelni profesjonalnie!\r\n.\r\n"

skrzynka_pocztowa[
    3] = "+OK 1000 octets\r\nFrom: admin@serwer.pl\r\nSubject: Obrazek testowy\r\nMIME-Version: 1.0\r\nContent-Type: multipart/mixed; boundary=sep\r\n\r\n--sep\r\nContent-Type: text/plain\r\n\r\nOto Twoj obrazek w zalaczniku.\r\n\r\n--sep\r\nContent-Type: image/gif; name=\"test_zad11.gif\"\r\nContent-Disposition: attachment; filename=\"test_zad11.gif\"\r\nContent-Transfer-Encoding: base64\r\n\r\nR0lGODlhAQABAIAAAAUEBAAAACwAAAAAAQABAAACAkQBADs=\r\n--sep--\r\n.\r\n"

skrzynka_pocztowa[
    8] = "+OK 1257 octets\r\nFrom: test@interia.pl\r\nSubject: Test\r\n\r\nTresc wiadomosci numer 8 (Z przykladu z instrukcji).\r\n.\r\n"
skrzynka_pocztowa[
    11] = "+OK 50 octets\r\nFrom: spam@spam.pl\r\nSubject: Najmniejsza\r\n\r\nTo jest najmniejsza wiadomosc (do usuniecia).\r\n.\r\n"
skrzynka_pocztowa[
    17] = "+OK 2376 octets\r\nFrom: wykladowca@uczelnia.pl\r\nSubject: Najwieksza\r\n\r\nTo jest najwieksza wiadomosc w calej skrzynce (Zadanie 4).\r\n.\r\n"

print(f"Baza gotowa. Serwer oczekuje na polaczenie na {HOST}:{PORT}")

conn, addr = server_socket.accept()
print(f"\nPolaczono z klientem, Adres: {addr}")
conn.send(b"+OK POP3 server ready\r\n")

file_in = conn.makefile('r', encoding='utf-8')

for line in file_in:
    tekst = line.strip()
    if not tekst:
        continue

    print(f"Klient: {tekst}")
    komenda = tekst.upper()

    if komenda.startswith("USER"):
        conn.send(b"+OK User accepted\r\n")

    elif komenda.startswith("PASS"):
        conn.send(b"+OK Welcome. You have 17 messages.\r\n")

    elif komenda.startswith("STAT"):
        conn.send(b"+OK 17 22846\r\n")

    elif komenda.startswith("LIST"):
        print("Wysylam liste 17 wiadomosci")
        lista = "+OK Scan list follows:\r\n1 1321\r\n2 1319\r\n3 1319\r\n4 1337\r\n5 1311\r\n6 1255\r\n7 1255\r\n8 1257\r\n9 1255\r\n10 1255\r\n11 1253\r\n12 1255\r\n13 1257\r\n14 1255\r\n15 1311\r\n16 1255\r\n17 2376\r\n.\r\n"
        conn.send(lista.encode())

    elif komenda.startswith("RETR "):
        try:
            numer_str = komenda.split()[1]
            numer = int(numer_str)

            if numer in skrzynka_pocztowa:
                print(f"Znaleziono wiadomosc nr {numer}")
                conn.send(skrzynka_pocztowa[numer].encode())
            else:
                print(f"Blad: Wiadomosc nr {numer} nie istnieje!")
                conn.send(b"-ERR no such message\r\n")
        except Exception:
            print("Blad w skladni komendy RETR.")
            conn.send(b"-ERR invalid command format\r\n")

    elif komenda.startswith("DELE "):
        print("Usuniecie wiadomosci")
        conn.send(b"+OK message deleted\r\n")

    elif komenda.startswith("QUIT"):
        print("Zamykniecie sesji")
        conn.send(b"+OK POP3 server signing off\r\n")
        break

    else:
        print("Wykryto nieznana komende.")
        conn.send(b"-ERR unknown command\r\n")

conn.close()
server_socket.close()
print("Serwer zakonczyl prace.")