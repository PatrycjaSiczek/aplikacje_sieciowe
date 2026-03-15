import socket

host = socket.gethostbyname('ntp.task.gda.pl')
port = 13
try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    data = sock.recv(1024)
    print("git")

except socket.error as e:
    print("blad")
finally:
    sock.close()



