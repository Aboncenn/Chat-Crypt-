#!/usr/bin/env python3
# coding: utf-8

import socket
import select
from threading import Thread
import sys
import base64
from Crypto.Cipher import AES
import hashlib

#GESTION DES ARGUMENTS DONNEES DANS LE TERMINAL
if len(sys.argv) != 5 and len(sys.argv) != 4:
    print("Correct usage: script, IP address, port number and pseudonyme")
    exit()

#Ajout info ip/port
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
# Ajout du pseudonyme
Pseudo = str(sys.argv[3])
# Ajout du mot de passe
if len(sys.argv) == 5:
    pasphrase = sys.argv[4].encode("utf-8");
    m = hashlib.md5()
    m.update(pasphrase)
    m = m.hexdigest()
    encryption_suite = AES.new(m, AES.MODE_CFB, 'This is an IV456')
else:
    pasphrase = 0;

# GESTION DES SOCKET
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.connect((IP_address, Port))

# GESTION PSEUDO
setPseudo = ("#pseudo="+Pseudo).encode("utf-8")
server.send(setPseudo)
# BOUCLE DE L'INFINIE
while True:

    #Code qui fonctione grace au pif gagnant
    sockets_list = [sys.stdin, server]
    read_sockets,write_socket, error_socket = select.select(sockets_list,[],[])
    #end of pif gagnant

    for socks in read_sockets:
        if socks == server:
            if pasphrase != 0:
                decryption_suite = AES.new(m, AES.MODE_CFB, 'This is an IV456')
                #si le pasphrase existe, on tente de décrypter le message
                message = socks.recv(2048)
                cipher_text1 = decryption_suite.decrypt(base64.b64decode(message))
                print(cipher_text1)
                sys.stdout.flush()
            else:
                #si le pasphrase n'existe pas, on ne tente même pas.
                message = socks.recv(2048)
                sys.stdout.flush()
        else:
            if pasphrase != 0:
                #si pasphrase est différent de nul, nous sommes en mode déchiffrage
                message = sys.stdin.readline().encode("utf-8")
                cipher_text = base64.b64encode(encryption_suite.encrypt(message))
                server.send(cipher_text)
                sys.stdout.write(Pseudo + " > ")
                sys.stdout.write(message.decode())
                sys.stdout.flush()
            else:
                #sinon, nous sommes en mode message en clair
                MessageClair = sys.stdin.readline().encode("utf-8")
                server.send(MessageClair)
                sys.stdout.write(Pseudo + " > ")
                sys.stdout.write(MessageClair.decode())
                sys.stdout.flush()
