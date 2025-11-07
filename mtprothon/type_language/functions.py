from .tlobject import TLObject
from .primitives import Int128


class ReqPqMulti(TLObject):
    ID = 0xbe7e8ef1

    conversion_types = [Int128]

    def __init__(self, nonce: int):
        self.nonce = nonce
