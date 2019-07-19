# coding=utf8
# server.py
import socket
# from socket import *
import struct
import datetime
from face_recog_system import FaceRecognition

import io
# import Image

# def getipaddrs(hostname):  # 只是为了显示IP，仅仅测试一下
#     result = socket.getaddrinfo(hostname, None, 0, socket.SOCK_STREAM)
#     return [x[4][0] for x in result]

# host = '172.20.10.2'  # 为空代表为本地host
# host = '192.168.31.154'
host = '10.128.246.101'
port = 9999  # Arbitrary non-privileged port
BUFSIZ = 1024
i = 1
# hostname = socket.gethostname()
# print('hosename', hostname)
# hostip = getipaddrs(hostname)
# print('host ip', hostip)

#  AF_INET 表示连接使用ipv4地址族  SOCK_STREAM表示用流式套接字
tcpSerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #创服务器套接字

# Get the size of the socket's send buffer
bufsize = tcpSerSocket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
print ("Buffer size [Before]:%d" %bufsize)
# tcpSerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpSerSocket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2 ** 18)

bufsize = tcpSerSocket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
print ("Buffer size [After]:%d" %bufsize)

# 将套接字绑定该地址
tcpSerSocket.bind((host, port))
# 开始监听TCP传入连接。参数指定在拒绝连接之前，操作系统可以挂起的最大连接数量。
tcpSerSocket.listen(4)

while True:
    print('\nWaiting for connection...')
    tcpCliSocket, addr = tcpSerSocket.accept()
    print('Connected with...', addr)

    # recv（param）用于接收对方发送的数据, param为缓冲区大小
    data = tcpCliSocket.recv(8)
    data_length = struct.unpack('>q', data)[0]  # read length first
    print(data_length)
    # print(data_length.decode())
    # print(len(data))
    unknown_path = '/Users/apple/Face Recognition/unknown/'
    TIMEFORMAT = '%m-%d-%H:%M:%S'
    theTime = datetime.datetime.now().strftime(TIMEFORMAT)
    pic_name = unknown_path + "unknown_face_" + theTime + '.png'
    f = open(pic_name, 'ab')
    # f = open("unknown_image1.png", "wb")

    while len(data) != 0:
        print("order: " + str(i))
        data = tcpCliSocket.recv(data_length)    # then read content according to data length
        # print(data)
        f.write(bytearray(data))
        i = i + 1

    f.close()

    i = 0
    start_recognition = FaceRecognition(pic_name)


    # send_data = 'get your data: ' + data + 'length:' + str(data_length)
    # tcpCliSocket.send(send_data.encode())
    # tcpCliSocket

tcpCliSocket.close()

