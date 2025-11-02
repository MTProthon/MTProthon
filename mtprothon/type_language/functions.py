from .tlobject import TLObject


class ReqPqMulti(TLObject):
    def __init__(self, nonce):
        self.nonce = nonce

    def serialize(self):
        constructor = bytes.fromhex('f18e7ebe')
        return constructor + self.nonce
