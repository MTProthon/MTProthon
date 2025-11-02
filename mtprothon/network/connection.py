import socket
import time


class Connection:
    HOST = "149.154.167.40"
    PORT = 443
    TIMEOUT = 20

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(self.TIMEOUT)

    def start(self):
        self.sock.connect((self.HOST, self.PORT))

    def stop(self):
        self.sock.close()

    def send(self, data: bytes):
        self.sock.send(data)

    def recv(self, bufsize: int) -> bytes:
        return self.sock.recv(bufsize)

    @staticmethod
    def generate_message_id() -> int:
        now = int(time.time())
        msg_id = now * (2 ** 32)
        msg_id = (msg_id // 4) * 4  # Message id must be divisible by 4
        return msg_id
