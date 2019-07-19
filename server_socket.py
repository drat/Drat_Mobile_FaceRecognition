# coding=utf8
# server.py
import socket
# from socket import *
import struct
import datetime
from face_recog_system import FaceRecognition


class Server:
    def __init__(self):
        # self.host = '10.128.246.101'
        # self.host = '192.168.31.154'    # 为空代表为本地host
        # self.host = '193.169.1.107'
        self.host = '10.128.244.202'
        self.port = 9999    # Arbitrary non-privileged port
        # 创建服务器套接字，AF_INET 表示连接使用ipv4地址族  SOCK_STREAM表示用流式套接字
        self.tcpSerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket_bind(self.host, self.port, self.tcpSerSocket)
        self.data_length = 0

    def get_ip_addrs(self, hostname):  # 只是为了显示IP，仅仅测试一下
        result = socket.getaddrinfo(hostname, None, 0, socket.SOCK_STREAM)
        return [x[4][0] for x in result]

    def set_buf_size(self):
        pass
        # Get the size of the socket's send buffer
        # buf_size = tcp_ser_socket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
        # print ("Buffer size [Before]:%d" %buf_size)

        # tcp_ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 2 ** 18)
        # buf_size = tcp_ser_socket.getsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF)
        # print ("Buffer size [After]:%d" %buf_size)

    def socket_bind(self, host, port, tcp_ser_socket):
        tcp_ser_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 将套接字绑定该地址
        tcp_ser_socket.bind((host, port))
        # 开始监听TCP传入连接。参数指定在拒绝连接之前，操作系统可以挂起的最大连接数量。
        tcp_ser_socket.listen(4)

        hostname = socket.gethostname()
        print('hostname: ', hostname)
        print('host ip: ', self.get_ip_addrs(hostname))
        self.wait_connection(tcp_ser_socket)

    def wait_connection(self, tcp_ser_socket):
        while True:
            print('\nWaiting for connection...')
            tcp_cli_socket, address = tcp_ser_socket.accept()
            print('Connected with...', address, " >--- mobile-end")
            pic_path_name = self.create_file_name()
            pic_file = open(pic_path_name, 'ab')

            self.receive_image(tcp_cli_socket, pic_file)
            pic_file.close()
            print("received successfully.\n")

            start_recognition = FaceRecognition()
            max_name_sim = start_recognition.face_classification(pic_path_name)
            self.send_data(tcp_cli_socket, max_name_sim)
            tcp_cli_socket.close()
            # 等待用户反馈
            feedback = self.receive_feedback(tcp_ser_socket)
            # 更新系统
            start_recognition.update_system(feedback,
                                            start_recognition.unknown_encoding,
                                            start_recognition.result_name,
                                            start_recognition.unknown_path)
            # tcp_ser_socket.close()

    def receive_image(self, tcp_cli_socket, pic_file):
        print(tcp_cli_socket)
        i = 0
        # use recv(param) to receive the length of the bytes stream first, which is 8 bytes
        data = tcp_cli_socket.recv(8)
        self.data_length = struct.unpack('>q', data)[0]  # read length first
        print("data size: " + str(self.data_length) + " Bytes")
        # repeatedly receive the content of the image
        while len(data) != 0:
            print("order: " + str(i))
            # then read content according to data length
            data = tcp_cli_socket.recv(self.data_length)
            pic_file.write(bytearray(data))
            i = i + 1

    def send_data(self, tcp_cli_socket, max_name_sim):
        print("\n" + max_name_sim)
        send_data = max_name_sim.encode()
        print(send_data)
        tcp_cli_socket.sendall(send_data)
        print("server sent data: " + str(send_data))

    def receive_feedback(self, tcpSerSock):
        print('\nNow waiting for feedback...')
        tcpCliSock, address = tcpSerSock.accept()
        # print(tcpCliSock)
        print('...connected with:', address, " >--- mobile-end")

        data = tcpCliSock.recv(8)
        data_length = struct.unpack('>q', data)[0]  # read length first
        print("data size: " + str(data_length))

        # 接收文字消息
        data = tcpCliSock.recv(data_length)
        data = data.decode()

        send_data = 'Server got your message: ' + str(data)
        # send_data = send_data.encode()
        tcpCliSock.send(send_data.encode())
        print(send_data)
        return data

    def create_file_name(self):
        # print(data_length.decode())
        # print(len(data))
        unknown_path = '/Users/apple/Face Recognition/unknown/'
        TIMEFORMAT = '%m-%d-%H:%M:%S'
        theTime = datetime.datetime.now().strftime(TIMEFORMAT)
        pic_path_name = unknown_path + "unknown_face_" + theTime + '.png'
        return pic_path_name


server = Server()

