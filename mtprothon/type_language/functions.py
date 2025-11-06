from .tlobject import TLObject


class ReqPqMulti(TLObject):
    ID = 0xbe7e8ef1

    def __init__(self, nonce):
        self.nonce = nonce

    def serialize(self) -> bytes:
        constructor = self.ID.to_bytes(length=4, byteorder="little")
        return constructor + self.nonce
