from .meta_schema_enum import MetaSchemaEnum, UNSPECIFIED_VALUE

class DataClassification(MetaSchemaEnum):
    UNSPECIFIED = UNSPECIFIED_VALUE
    PUBLIC = "Public"
    PRIVATE = "Private"
    INTERNAL = "Internal"
    CONFIDENTIAL = "Confidential"
    RESTRICTED = "Restricted"

