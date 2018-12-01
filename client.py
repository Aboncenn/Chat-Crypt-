import socket
import select
import sys
from Crypto.Cipher import AES
import hashlib
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if len(sys.argv) != 5 and len(sys.argv) != 4:
    print("Correct usage: script, IP address, port number and pseudonyme")
    exit()

#Ajout info ip/port
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.connect((IP_address, Port))
# Ajout du pseudonyme
Pseudo = str(sys.argv[3])
# Ajout de la passphrase
if len(sys.argv) == 5:
    pasphrase = sys.argv[4].encode("utf-8");
    m = hashlib.md5()
    m.update(pasphrase)
    m = m.hexdigest()
    encryption_suite = AES.new(m, AES.MODE_CFB, 'This is an IV456')
else:
    pasphrase = 0;

while True:

    # maintains a list of possible input streams
    sockets_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])

    for socks in read_sockets:
        if socks == server:
            message = socks.recv(2048)
            print(message)
        else:

            if pasphrase != 0:
                message = sys.stdin.readline().encode("utf-8")
                cipher_text = encryption_suite.encrypt(message)
                server.send(cipher_text)
                server.send(message)
                sys.stdout.write(Pseudo + " > ")
                sys.stdout.write(message.decode())
                sys.stdout.flush()
            else:
                message = sys.stdin.readline().encode("utf-8")
                server.send(message)
                sys.stdout.write(Pseudo + " > ")
                sys.stdout.write(message.decode())
                sys.stdout.flush()


server.close()
