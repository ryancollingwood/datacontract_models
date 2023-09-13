from .meta_schema_enum import MetaSchemaEnum

class DataClassification(MetaSchemaEnum):
    UNSPECIFIED = "unspecified"
    PUBLIC = "public"
    PRIVATE = "private"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

