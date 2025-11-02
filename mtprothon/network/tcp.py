import socket


class TCP:
    HOST = "149.154.167.40"
    PORT = 443
    TIMEOUT = 20

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.TIMEOUT)

    def connect(self):
        self.sock.connect((self.HOST, self.PORT))

    def disconnect(self):
        self.sock.close()

    def send(self, data: bytes):
        self.sock.send(data)

    def recv(self, bufsize: int = 0) -> bytes:
        return self.sock.recv(bufsize)
