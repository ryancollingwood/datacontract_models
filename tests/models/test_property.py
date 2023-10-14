from models import Property, Cardinality

from .test_property_attribute import reference_property_attribute
from .test_database_column import reference_database_column


reference_property = Property(
    cardinality=Cardinality.ONLY_ONE,
    attribute=reference_property_attribute,
    source=reference_database_column,
)


# TODO: More tests
def test_property():
    property = Property(
        cardinality=Cardinality.ONLY_ONE,
        attribute=reference_property_attribute,
        source=reference_database_column,
    )

    assert property.cardinality == Cardinality.ONLY_ONE


def test_property_is_identifier():
    property = Property(
        cardinality=Cardinality.ONLY_ONE,
        attribute=reference_property_attribute,
        source=reference_database_column,
    )

    assert property.is_identifier == False


def test_property_is_required():
    property = Property(
        cardinality=Cardinality.ONLY_ONE,
        attribute=reference_property_attribute,
        source=reference_database_column,
    )

    assert property.is_required == True
