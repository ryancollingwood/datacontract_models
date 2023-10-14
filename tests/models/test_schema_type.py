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
    ]


def test_schema_type_is_uid():
    assert SchemaType.UNSPECIFIED.is_uid() == False
    assert SchemaType.STR.is_uid() == False
    assert SchemaType.GUID.is_uid() == True
    assert SchemaType.UUID.is_uid() == True
    assert SchemaType.INT.is_uid() == False
    assert SchemaType.DECIMAL.is_uid() == False


def test_schema_type_repr():
    assert repr(SchemaType.UNSPECIFIED) == "SchemaType.UNSPECIFIED"
    assert repr(SchemaType.STR) == "SchemaType.STR"
    assert repr(SchemaType.GUID) == "SchemaType.GUID"
    assert repr(SchemaType.UUID) == "SchemaType.UUID"
    assert repr(SchemaType.INT) == "SchemaType.INT"
    assert repr(SchemaType.DECIMAL) == "SchemaType.DECIMAL"


def test_schema_type_is_specified():
    assert SchemaType.UNSPECIFIED.is_specified() == False
    assert SchemaType.STR.is_specified() == True
    assert SchemaType.GUID.is_specified() == True
    assert SchemaType.UUID.is_specified() == True
    assert SchemaType.INT.is_specified() == True
    assert SchemaType.DECIMAL.is_specified() == True

