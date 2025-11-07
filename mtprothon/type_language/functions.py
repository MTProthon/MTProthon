from .tlobject import TLObject
from .primitives import Int128, Bytes, Long


class ReqPqMulti(TLObject):
    ID = 0xbe7e8ef1

    conversion_types = [Int128]

    def __init__(self, nonce: int):
        self.nonce = nonce


class ReqDHParams(TLObject):
    ID = 0xd712e4be

    conversion_types = [Int128, Int128, Bytes, Bytes, Long, Bytes]

    def __init__(self, nonce: int, server_nonce: int, p: bytes, q: bytes, public_key_fingerprint: int, encrypted_data: bytes):
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.p = p
        self.q = q
        self.public_key_fingerprint = public_key_fingerprint
        self.encrypted_data = encrypted_data


class SetClientDHParams(TLObject):
    ID = 0xf5045f1f

    conversion_types = [Int128, Int128, Bytes]

    def __init__(self, nonce: int, server_nonce: int, encrypted_data: bytes):
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.encrypted_data = encrypted_data
