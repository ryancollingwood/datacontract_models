from .meta_schema_enum import MetaSchemaEnum, UNSPECIFIED_VALUE


class SchemaType(MetaSchemaEnum):
    UNSPECIFIED = UNSPECIFIED_VALUE
    STR = "str"
    GUID = "guid"
    UUID = "uuid"
    INT = "int"
    DECIMAL = "decimal"

    def is_unique(self):
        return self in [SchemaType.UUID, SchemaType.GUID]
