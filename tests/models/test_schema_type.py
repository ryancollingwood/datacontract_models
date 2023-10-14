from models import SchemaType


def test_schema_type_values():
    options = [x.value for x in SchemaType]
    assert options == [
        "UNSPECIFIED",
        "str",
        "guid",
        "uuid",
        "int",
        "decimal",
        "float",
        "boolean",
        "date",
        "datetime",
        "time",
        "timestamp",
        "utc_timestamp",
        "epoch_timestamp",
    ]


def test_schema_type_is_uid():
    assert SchemaType.UNSPECIFIED.is_uid() == False
    assert SchemaType.STR.is_uid() == False
    assert SchemaType.GUID.is_uid() == True
    assert SchemaType.UUID.is_uid() == True
    assert SchemaType.INT.is_uid() == False
    assert SchemaType.DECIMAL.is_uid() == False
    assert SchemaType.BOOLEAN.is_uid() == False
    assert SchemaType.DATE.is_uid() == False
    assert SchemaType.DATETIME.is_uid() == False
    assert SchemaType.TIME.is_uid() == False
    assert SchemaType.TIMESTAMP.is_uid() == False
    assert SchemaType.UTC_TIMESTAMP.is_uid() == False
    assert SchemaType.EPOCH_TIMESTAMP.is_uid() == False


def test_schema_type_repr():
    assert repr(SchemaType.UNSPECIFIED) == "SchemaType.UNSPECIFIED"
    assert repr(SchemaType.STR) == "SchemaType.STR"
    assert repr(SchemaType.GUID) == "SchemaType.GUID"
    assert repr(SchemaType.UUID) == "SchemaType.UUID"
    assert repr(SchemaType.INT) == "SchemaType.INT"
    assert repr(SchemaType.DECIMAL) == "SchemaType.DECIMAL"
    assert repr(SchemaType.BOOLEAN) == "SchemaType.BOOLEAN"
    assert repr(SchemaType.DATE) == "SchemaType.DATE"
    assert repr(SchemaType.DATETIME) == "SchemaType.DATETIME"
    assert repr(SchemaType.TIME) == "SchemaType.TIME"
    assert repr(SchemaType.TIMESTAMP) == "SchemaType.TIMESTAMP"
    assert repr(SchemaType.EPOCH_TIMESTAMP) == "SchemaType.EPOCH_TIMESTAMP"
    assert repr(SchemaType.UTC_TIMESTAMP) == "SchemaType.UTC_TIMESTAMP"


def test_schema_type_is_specified():
    assert SchemaType.UNSPECIFIED.is_specified() == False
    assert SchemaType.STR.is_specified() == True
    assert SchemaType.GUID.is_specified() == True
    assert SchemaType.UUID.is_specified() == True
    assert SchemaType.INT.is_specified() == True
    assert SchemaType.DECIMAL.is_specified() == True
    assert SchemaType.BOOLEAN.is_specified() == True
    assert SchemaType.DATE.is_specified() == True
    assert SchemaType.DATETIME.is_specified() == True
    assert SchemaType.TIME.is_specified() == True
    assert SchemaType.TIMESTAMP.is_specified() == True
    assert SchemaType.UTC_TIMESTAMP.is_specified() == True
    assert SchemaType.EPOCH_TIMESTAMP.is_specified() == True


def test_schema_type_is_temporal():
    assert SchemaType.UNSPECIFIED.is_temporal() == False
    assert SchemaType.STR.is_temporal() == False
    assert SchemaType.GUID.is_temporal() == False
    assert SchemaType.UUID.is_temporal() == False
    assert SchemaType.INT.is_temporal() == False
    assert SchemaType.DECIMAL.is_temporal() == False
    assert SchemaType.BOOLEAN.is_temporal() == False
    assert SchemaType.DATE.is_temporal() == True
    assert SchemaType.DATETIME.is_temporal() == True
    assert SchemaType.TIME.is_temporal() == True
    assert SchemaType.TIMESTAMP.is_temporal() == True
    assert SchemaType.UTC_TIMESTAMP.is_temporal() == True
    assert SchemaType.EPOCH_TIMESTAMP.is_temporal() == True


def test_schema_type_is_timestamp():
    assert SchemaType.UNSPECIFIED.is_timestamp() == False
    assert SchemaType.STR.is_timestamp() == False
    assert SchemaType.GUID.is_timestamp() == False
    assert SchemaType.UUID.is_timestamp() == False
    assert SchemaType.INT.is_timestamp() == False
    assert SchemaType.DECIMAL.is_timestamp() == False
    assert SchemaType.BOOLEAN.is_timestamp() == False
    assert SchemaType.DATE.is_timestamp() == False
    assert SchemaType.DATETIME.is_timestamp() == False
    assert SchemaType.TIME.is_timestamp() == False
    assert SchemaType.TIMESTAMP.is_timestamp() == True
    assert SchemaType.UTC_TIMESTAMP.is_timestamp() == True
    assert SchemaType.EPOCH_TIMESTAMP.is_timestamp() == True


def test_schema_type_is_numeric():
    assert SchemaType.UNSPECIFIED.is_numeric() == False
    assert SchemaType.STR.is_numeric() == False
    assert SchemaType.GUID.is_numeric() == False
    assert SchemaType.UUID.is_numeric() == False
    assert SchemaType.INT.is_numeric() == True
    assert SchemaType.DECIMAL.is_numeric() == True
    assert SchemaType.BOOLEAN.is_numeric() == False
    assert SchemaType.DATE.is_numeric() == False
    assert SchemaType.DATETIME.is_numeric() == False
    assert SchemaType.TIME.is_numeric() == False
    assert SchemaType.TIMESTAMP.is_numeric() == False
    assert SchemaType.UTC_TIMESTAMP.is_numeric() == False
    assert SchemaType.EPOCH_TIMESTAMP.is_numeric() == False

