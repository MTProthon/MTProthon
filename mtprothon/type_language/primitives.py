from io import BytesIO
import struct

from .tlobject import TLObject


class Primitive(TLObject):
    def __init__(self, value):
        self.value = value


class Int(Primitive):
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


class Double(Primitive):
    def serialize(self):
        return struct.pack('<d', self.value)

    @classmethod
    def deserialize(cls, data: BytesIO):
        return struct.unpack('<d', data.read(8))[0]


class Bool(Primitive):
    BOOL_TRUE = 0x997275b5
    BOOL_FALSE = 0xbc799737

    def serialize(self) -> bytes:
        constructor_id = self.BOOL_TRUE if self.value else self.BOOL_FALSE
        return Int(constructor_id).serialize(signed=False)

    @classmethod
    def deserialize(cls, data: BytesIO) -> bool:
        return Int.deserialize(data, signed=False) == cls.BOOL_TRUE


class Bytes(Primitive):
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
        first_byte_data = data.read(1)
        first_byte = first_byte_data[0]

        if first_byte <= 253:
            length = first_byte
            length_bytes_read = 1
        else:
            length_data = data.read(3)
            length = int.from_bytes(length_data, 'little')
            length_bytes_read = 4

        result = data.read(length)

        total_read = length_bytes_read + length
        padding = (4 - (total_read % 4)) % 4
        data.read(padding)

        return result


class String(Bytes):
    def serialize(self) -> bytes:
        self.value = self.value.encode("utf-8")
        return super().serialize()

    @classmethod
    def deserialize(cls, data: BytesIO) -> str:
        return super().deserialize(data).decode(errors="replace")


class Vector(Primitive):
    ID = 0x1CB5C415

    def __class_getitem__(cls, item):
        return cls(t=item)

    def __init__(self, value=None, *, t=None):
        self.value = value
        self.t = t

    def serialize(self) -> bytes:
        result = Int(self.ID).serialize()
        result += Int(len(self.value)).serialize()

        for item in self.value:
            result += item.serialize()

        return result

    def deserialize(self, data: BytesIO) -> list:
        constructor = Int.deserialize(data)
        count = Int.deserialize(data)

        items = []
        for _ in range(count):
            item = self.t.deserialize(data)
            items.append(item)

        return items
