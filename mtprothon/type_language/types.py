from .tlobject import TLObject
from .primitives import Bytes, Vector, Long


class ResPQ(TLObject):
    ID = 0x05162463

    def __init__(self, nonce, server_nonce, pq, fingerprints):
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.pq = pq
        self.fingerprints = fingerprints

    @classmethod
    def deserialize(cls, data):
        constructor = data.read(4)
        expected = bytes.fromhex('63241605')  # 05162463 in little-endian
        if constructor != expected:
            raise ValueError(f"Expected resPQ constructor, got {constructor.hex()}")

        nonce = data.read(16)
        if len(nonce) < 16:
            raise ValueError("Not enough data for nonce")

        server_nonce = data.read(16)
        if len(server_nonce) < 16:
            raise ValueError("Not enough data for server_nonce")

        pq = Bytes.deserialize(data)
        fingerprints = Vector.deserialize(data, Long)
        return cls(nonce, server_nonce, pq, fingerprints)
