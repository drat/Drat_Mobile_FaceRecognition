# server.py
from socket import *

def getipaddrs(hostname):  # 只是为了显示IP，仅仅测试一下
    result = socket.getaddrinfo(hostname, None, 0, socket.SOCK_STREAM)
    return [x[4][0] for x in result]

host = '10.128.237.246'  # 为空代表为本地host
hostname = socket.gethostname()
print('hosename', hostname)
hostip = getipaddrs(hostname)
print('host ip', hostip)  # 应该显示为：127.0.1.1
port = 9999  # Arbitrary non-privileged port
tcpSerSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpSerSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
tcpSerSocket.bind((host, port))
tcpSerSocket.listen(4)
while True:
    print('Waiting for connection...')
    tcpCliSocket, addr = tcpSerSocket.accept()
    print('Connected by', addr)
    data = conn.recv(1024)
    if not data: break
    conn.sendall(data)  # 把接收到数据原封不动的发送回去
    print('Received', repr(data))
    conn.close()