# # !/usr/bin/env python
#
# from socket import *
#
# HOST = '172.20.10.2'
# PORT = 9999
# BUFSIZ = 1024
# ADDR = (HOST, PORT)
#
# tcpCliSock = socket(AF_INET, SOCK_STREAM)
# tcpCliSock.connect(ADDR)
#
# while True:
#     # data = input('> ')
#     # if not data:
#     #     break
#     # tcpCliSock.send(data.encode())
#     f = open("test.jpg", mode='rb')
#     tcpCliSock.sendfile(f)
#
#     recv_data = tcpCliSock.recv(BUFSIZ)
#     recv_data = recv_data.decode()
#
#     if not recv_data:
#         break
#     print(recv_data)
#
# tcpCliSock.close()

str = "Line1-abcdef"
print(str.split('-')[0])       # 以空格为分隔符，包含 \n
# print(str.split(' ', 1) # 以空格为分隔符，分隔成两个