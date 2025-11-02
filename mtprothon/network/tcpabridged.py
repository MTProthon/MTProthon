from .tcp import TCP


class TCPAbridged(TCP):
    def connect(self):
        super().connect()
        super().send(b'\xef')

    def send(self, data: bytes):
        if len(data) % 4 != 0:
            raise ValueError("Message length must be divisible by 4")

        length_value = len(data) // 4

        if length_value <= 126:
            data = bytes([length_value]) + data
        else:
            data = b'\x7f' + length_value.to_bytes(3, 'little') + data

        super().send(data)

    def recv(self, bufsize: int) -> bytes:
        length_byte = super().recv(1)[0]

        if length_byte <= 126:
            message_length = length_byte * 4
        elif length_byte == 0x7f:
            length_bytes = super().recv(3)
            message_length = int.from_bytes(length_bytes, 'little') * 4
        else:
            raise ValueError(f"Invalid length byte: {length_byte}")

        data = b''
        while len(data) < message_length:
            chunk = super().recv(message_length - len(data))
            if not chunk:
                raise ConnectionError("Connection closed")
            data += chunk

        return data
