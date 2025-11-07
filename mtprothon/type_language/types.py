from typing import List

from .tlobject import TLObject
from .primitives import Bytes, Vector, Long, Int128, Int256, Int


class ResPQ(TLObject):
    ID = 0x05162463

    conversion_types = [Int128, Int128, Bytes, Vector[Long]]

    def __init__(self, nonce: int, server_nonce: int, pq: bytes, fingerprints: List[int]):
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.pq = pq
        self.fingerprints = fingerprints


class PQInnerData(TLObject):
    ID = 0x83c95aec

    conversion_types = [Bytes, Bytes, Bytes, Int128, Int128, Int256]

    def __init__(self, pq: bytes, p: bytes, q: bytes, nonce: int, server_nonce: int, new_nonce: int):
        self.pq = pq
        self.p = p
        self.q = q
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.new_nonce = new_nonce


class ServerDHParamsOk(TLObject):
    ID = 0xd0e8075c

    conversion_types = [Int128, Int128, Bytes]

    def __init__(self, nonce: int, server_nonce: int, encrypted_answer: bytes):
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.encrypted_answer = encrypted_answer


class ServerDHInnerData(TLObject):
    ID = 0xb5890dba

    conversion_types = [Int128, Int128, Int, Bytes, Bytes, Int]

    def __init__(self, nonce: int, server_nonce: int, g: int, dh_prime: bytes, g_a: bytes, server_time: int):
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.g = g
        self.dh_prime = dh_prime
        self.g_a = g_a
        self.server_time = server_time


class ClientDHInnerData(TLObject):
    ID = 0x6643b654

    conversion_types = [Int128, Int128, Long, Bytes]

    def __init__(self, nonce: int, server_nonce: int, retry_id: int, g_b: bytes):
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.retry_id = retry_id
        self.g_b = g_b


class DHGenOk(TLObject):
    ID = 0x3bcbf734

    conversion_types = [Int128, Int128, Int128]

    def __init__(self, nonce: int, server_nonce: int, new_nonce_hash1: int):
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.new_nonce_hash1 = new_nonce_hash1
