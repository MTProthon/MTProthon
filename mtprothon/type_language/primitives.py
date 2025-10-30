from io import BytesIO

from .tlobject import TLObject


class Int(TLObject):
    LENGTH = 4

    def serialize(self) -> bytes:
        return self.value.to_bytes(self.LENGTH, byteorder="little", signed=True)

    @classmethod
    def deserialize(cls, data: BytesIO) -> int:
        return int.from_bytes(data.read(cls.LENGTH), byteorder="little", signed=True)


class Long(Int):
    LENGTH = 8


class Int128(Int):
    LENGTH = 16


class Int256(Int):
    LENGTH = 32
