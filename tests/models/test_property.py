from models import Property, Cardinality, PropertyAttribute, SemanticType, Variety

from .test_property_attribute import reference_property_attribute
from .test_database_column import reference_database_column, boolean_database_column


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


def test_property_is_boolean_and_limited_variety():
    """
    This contradictory specification of a schema type that is boolean
    but a variety that is not a limited subset, must be corrected
    by the Property validator
    """
    property = Property(
        cardinality=Cardinality.ONLY_ONE,
        attribute=PropertyAttribute(
            name="IsActive",
            semantic_type=SemanticType(
                name="Checkbox",
                variety=Variety.UNSPECIFIED
            )
        ),
        source=boolean_database_column
    )

    assert property.attribute.semantic_type.variety == Variety.LIMITED_SUBSET, "Booleans must mean a limited subset"