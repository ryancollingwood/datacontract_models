from .meta_schema_enum import MetaSchemaEnum, UNSPECIFIED_VALUE


class SchemaType(MetaSchemaEnum):
    UNSPECIFIED = UNSPECIFIED_VALUE
    STR = "str"
    GUID = "guid"
    UUID = "uuid"
    INT = "int"
    DECIMAL = "decimal"
    FLOAT = "float"
    TIMESTAMP = "timestamp"
    UTC_TIMESTAMP = "utc_timestamp"
    EPOCH_TIMESTAMP = "epoch_timestamp"
    DATE = "date"
    TIME = "time"

    def is_uid(self):
        """
        Returns True if value is result of function to generate
        unique values, such as UUID or GUID
        """
        return self in [SchemaType.UUID, SchemaType.GUID]

    def is_numeric(self):
        """
        Returns True if value is numeric,
        regardless of decimal places or precision
        """
        return self in [SchemaType.INT, SchemaType.DECIMAL, SchemaType.FLOAT]

    def is_temporal(self):
        """
        Returns True if value is representing a point in time,
        regardless of precision or timezone
        """
        return self in [
            SchemaType.TIMESTAMP,
            SchemaType.UTC_TIMESTAMP,
            SchemaType.EPOCH_TIMESTAMP,
            SchemaType.DATE,
            SchemaType.TIME,
        ]

    def is_timestamp(self):
        """
        Returns True if value is representing a point in time 
        having a date component and a time component,
        regardless of precision or timezone
        """
        return self in [
            SchemaType.TIMESTAMP,
            SchemaType.UTC_TIMESTAMP,
            SchemaType.EPOCH_TIMESTAMP,
        ]
