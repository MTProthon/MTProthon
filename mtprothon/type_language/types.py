from typing import List

from .tlobject import TLObject
from .primitives import Bytes, Vector, Long, Int128


class ResPQ(TLObject):
    ID = 0x05162463

    tl_types = [Int128, Int128, Bytes, Vector[Long]]

    def __init__(self, nonce: int, server_nonce: int, pq: bytes, fingerprints: List[int]):
        self.nonce = nonce
        self.server_nonce = server_nonce
        self.pq = pq
        self.fingerprints = fingerprints
