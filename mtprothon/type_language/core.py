from io import BytesIO

from .tlobject import TLObject
from .primitives import Long, Int


class Message(TLObject):
    def __init__(self, auth_key_id: bytes, id: int, length: int, data: bytes):
        self.auth_key_id = auth_key_id
        self.id = id
        self.length = length
        self.data = data

    def serialize(self) -> bytes:
        return self.auth_key_id + Long(self.id).serialize() + Int(self.length).serialize() + self.data

    @classmethod
    def deserialize(cls, data: BytesIO) -> "Message":
        auth_key_id = data.read(8)

        id = Long.deserialize(data)

        length = Int.deserialize(data)

        payload = data.read(length)
        if len(payload) < length:
            raise ValueError(f"Expected {length} bytes, got {len(payload)}")

        return cls(auth_key_id, id, length, payload)
