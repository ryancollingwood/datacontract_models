from .meta_schema_enum import MetaSchemaEnum, UNSPECIFIED_VALUE


class MetaTiming(MetaSchemaEnum):
    """
    MetaTiming is an enumeration of the different types of timing
    relating to the handling of data for a given value
    
    - UNSPECIFIED: The value has no specified relevance to the 
        handling of data
    - CAPTURE: The value details when the data was captured,
        covering creation, modification, or deletion
    - PERSISTED: The value details when the data was persisted
        covering both the case of original data being persisted, and
        the case of the data being copied
    - EMISSION:The value details the time of the data being emitted
        from a source system, such as a message queue
    """
    UNSPECIFIED = UNSPECIFIED_VALUE
    CAPTURE = "Capture"
    PERSISTED = "Persisted"
    EMISSION = "Emission"
