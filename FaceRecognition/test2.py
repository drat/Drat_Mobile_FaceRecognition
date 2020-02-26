#!/usr/bin/env python

from socket import *
from time import ctime

HOST = '10.128.237.246'
PORT = 9999
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)

while True:
    print ('waiting for connection...')
    tcpCliSock, addr = tcpSerSock.accept()
    print(tcpCliSock)
    print ('...connected from:', addr)

    while True:
        data = tcpCliSock.recv(BUFSIZ)
        print(data)
        data = data.decode()
        print(data)
        if not data:
            break
        send_data = 'get your data: ' + data
        tcpCliSock.send(send_data.encode())

    tcpCliSock.close()

# tcpSerSock.close()
