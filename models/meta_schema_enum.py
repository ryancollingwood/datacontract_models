import enum

class MetaSchemaEnum(enum.Enum):
    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return f"{type(self).__name__}.{str(self.name)}"
