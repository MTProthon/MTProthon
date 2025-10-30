from io import BytesIO
import struct

from .tlobject import TLObject


class Int(TLObject):
    LENGTH = 4

    def serialize(self, signed: bool = True) -> bytes:
        return self.value.to_bytes(self.LENGTH, byteorder="little", signed=signed)

    @classmethod
    def deserialize(cls, data: BytesIO, signed: bool = True) -> int:
        return int.from_bytes(data.read(cls.LENGTH), byteorder="little", signed=signed)


class Long(Int):
    LENGTH = 8


class Int128(Int):
    LENGTH = 16


class Int256(Int):
    LENGTH = 32


class Double(TLObject):
    def serialize(self):
        return struct.pack('<d', self.value)

    @classmethod
    def deserialize(cls, data: BytesIO):
        return struct.unpack('<d', data.read(8))[0]


class Bool(TLObject):
    BOOL_TRUE = 0x997275b5
    BOOL_FALSE = 0xbc799737

    def serialize(self) -> bytes:
        constructor_id = self.BOOL_TRUE if self.value else self.BOOL_FALSE
        return Int(constructor_id).serialize(signed=False)

    @classmethod
    def deserialize(cls, data: BytesIO) -> bool:
        return Int.deserialize(data, signed=False) == cls.BOOL_TRUE


class Bytes(TLObject):
    def serialize(self) -> bytes:
        length = len(self.value)

        if length <= 253:
            result = bytes([length]) + self.value
        else:
            result = b"\xfe" + length.to_bytes(length=3, byteorder="little") + self.value

        current_length = len(result)
        padding_needed = (4 - (current_length % 4)) % 4
        result += b"\x00" * padding_needed
        return result

    @classmethod
    def deserialize(cls, data: BytesIO) -> bytes:
        first_byte = int.from_bytes(data.read(1), byteorder="little")

        if first_byte <= 253:
            length = first_byte
        else:
            length = int.from_bytes(data.read(3), byteorder="little")

        return data.read(length)


class String(Bytes):
    def serialize(self) -> bytes:
        self.value = self.value.encode("utf-8")
        return super().serialize()

    @classmethod
    def deserialize(cls, data: BytesIO) -> str:
        return super().deserialize(data).decode(errors="replace")


class Vector(TLObject):
    ID = 0x1CB5C415

    def serialize(self):
        result = Int(self.ID).serialize()
        result += Int(len(self.value)).serialize()

        for item in self.value:
            result += item.serialize()

        return result

    @classmethod
    def deserialize(cls, data: BytesIO, type):
        constructor = Int.deserialize(data)
        count = Int.deserialize(data)

        items = []
        for _ in range(count):
            item = type.deserialize(data)
            items.append(item)

        return items
