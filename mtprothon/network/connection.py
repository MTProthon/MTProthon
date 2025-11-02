import typing
import time

from .tcp import TCP
from .tcpabridged import TCPAbridged


class Connection:
    def __init__(self, tcp: typing.Type[TCP] = TCPAbridged):
        self.tcp = tcp()

    def start(self):
        self.tcp.connect()

    def stop(self):
        self.tcp.disconnect()

    def send(self, data: bytes):
        self.tcp.send(data)

    def recv(self, bufsize: int) -> bytes:
        return self.tcp.recv(bufsize)

    @staticmethod
    def generate_message_id() -> int:
        now = int(time.time())
        msg_id = now * (2 ** 32)
        msg_id = (msg_id // 4) * 4  # Message id must be divisible by 4
        return msg_id
