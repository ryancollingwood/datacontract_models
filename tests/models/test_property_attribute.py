from models import PropertyAttribute, SemanticType, Variety
from .test_semantic_type import reference_semantic_type


reference_property_attribute = PropertyAttribute(
    name="Invoice Total",
    semantic_type=reference_semantic_type
    )


def test_property_attribute():
    property_attribute = PropertyAttribute(
        name="Invoice Total",
        semantic_type=reference_semantic_type
        )
    
    assert property_attribute.name == "Invoice Total"
    assert property_attribute.semantic_type.name == "Money"


def test_property_attribute_repr():
    property_attribute = PropertyAttribute(
        name="Invoice Total",
        semantic_type=reference_semantic_type
        )
    
    assert repr(property_attribute) == "PropertyAttribute(name='Invoice Total', semantic_type=SemanticType(name='Money', classification=DataClassification.UNSPECIFIED, variety=Variety.VARIABLE))"


def test_property_attribute_extra_attributes():
    property_attribute = PropertyAttribute(
        name="Invoice Total",
        semantic_type=reference_semantic_type,
        extra="extra"
        )
    
    assert property_attribute.extra == "extra"


def test_property_attribute_to_contract():
    property_attribute = PropertyAttribute(
        name="Invoice Total",
        semantic_type=reference_semantic_type,
        extra="extra"
        )
    
    assert property_attribute.to_contract() == {
        'name': 'Invoice Total',
        'semantic_type': 'Money',
        'classification': 'UNSPECIFIED', 
        'variety': 'Variable',
        'extra': 'extra',
        }

