from .meta_schema_enum import MetaSchemaEnum, UNSPECIFIED_VALUE

class DataClassification(MetaSchemaEnum):
    UNSPECIFIED = UNSPECIFIED_VALUE
    PUBLIC = "public"
    PRIVATE = "private"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

