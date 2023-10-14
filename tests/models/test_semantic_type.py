from models import SemanticType, DataClassification, Variety


reference_semantic_type = SemanticType(
    name="Money",
    variety=Variety.VARIABLE,
    )


def test_semantic_type():
    semantic_type = SemanticType(name="Money")
    assert semantic_type.name == "Money"
    assert semantic_type.classification == DataClassification.UNSPECIFIED
    assert semantic_type.variety == Variety.UNSPECIFIED


def test_semantic_type_repr():
    semantic_type = SemanticType(name="Money")
    assert repr(semantic_type) == "SemanticType(name='Money', classification=DataClassification.UNSPECIFIED, variety=Variety.UNSPECIFIED)"


def test_semantic_type_extra_attributes():
    semantic_type = SemanticType(name="Money", extra="extra")
    assert semantic_type.extra == "extra"


def test_semantic_type_classification():
    semantic_type = SemanticType(name="Money", classification=DataClassification.PUBLIC)
    assert semantic_type.classification == DataClassification.PUBLIC


def test_semantic_type_variety():
    semantic_type = SemanticType(name="Money", variety=Variety.VARIABLE)
    assert semantic_type.variety == Variety.VARIABLE


def test_semantic_type_to_contract():
    semantic_type = SemanticType(name="Money", variety=Variety.VARIABLE)
    assert semantic_type.to_contract() == {
        "name": "Money",
        "classification": "UNSPECIFIED",
        "variety": "Variable",
    }