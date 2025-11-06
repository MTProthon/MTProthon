from io import BytesIO


class TLObject:
    ID: int

    tl_types = []

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def get_tl_types(cls):
        return cls.tl_types

    def get_values(self):
        return self.__dict__.values()

    @classmethod
    def deserialize(cls, data: BytesIO) -> "TLObject":
        constructor = data.read(4)

        if constructor != cls.ID.to_bytes(length=4, byteorder="little"):
            raise ValueError(f"Expected {TLObject.__name__} constructor, got {constructor.hex()}")

        return cls(*[t.deserialize(data) for t in cls.get_tl_types()])
