from io import BytesIO
from typing import List


class TLObject:
    ID: int

    conversion_types: List["TLObject"]

    def get_values(self):
        return self.__dict__.values()

    def serialize(self) -> bytes:
        buffer = BytesIO()

        buffer.write(self.ID.to_bytes(length=4, byteorder="little"))

        for t, value in zip(self.conversion_types, self.get_values()):
            buffer.write(t(value).serialize())

        return buffer.getvalue()

    @classmethod
    def deserialize(cls, data: BytesIO) -> "TLObject":
        constructor = data.read(4)

        if constructor != cls.ID.to_bytes(length=4, byteorder="little"):
            raise ValueError(f"Expected {cls.__name__} constructor, got {constructor.hex()}")

        return cls(*[t.deserialize(data) for t in cls.conversion_types])
