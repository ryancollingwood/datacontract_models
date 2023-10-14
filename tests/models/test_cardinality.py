from models import Cardinality


def test_cardinality_values():
    options = [x.value for x in Cardinality]
    assert options == [
        "OnlyOne",
        "OneOrMore",
        "ZeroOrOne",
        "ZeroOrMany",
    ]


def test_cardinality_is_mandatory():
    assert Cardinality.ONLY_ONE.is_mandatory() == True
    assert Cardinality.ONE_OR_MORE.is_mandatory() == True
    assert Cardinality.ZERO_OR_ONE.is_mandatory() == False
    assert Cardinality.ZERO_OR_MANY.is_mandatory() == False


def test_cardinality_is_optional():
    assert Cardinality.ONLY_ONE.is_optional() == False
    assert Cardinality.ONE_OR_MORE.is_optional() == False
    assert Cardinality.ZERO_OR_ONE.is_optional() == True
    assert Cardinality.ZERO_OR_MANY.is_optional() == True


def test_cardinality_is_singular():
    assert Cardinality.ONLY_ONE.is_singular() == True
    assert Cardinality.ONE_OR_MORE.is_singular() == False
    assert Cardinality.ZERO_OR_ONE.is_singular() == True
    assert Cardinality.ZERO_OR_MANY.is_singular() == False


def test_cardinality_repr():
    assert repr(Cardinality.ONLY_ONE) == "Cardinality.ONLY_ONE"
    assert repr(Cardinality.ONE_OR_MORE) == "Cardinality.ONE_OR_MORE"
    assert repr(Cardinality.ZERO_OR_ONE) == "Cardinality.ZERO_OR_ONE"
    assert repr(Cardinality.ZERO_OR_MANY) == "Cardinality.ZERO_OR_MANY"


def test_cardinality_is_specified():
    assert Cardinality.ONLY_ONE.is_specified() == True
    assert Cardinality.ONE_OR_MORE.is_specified() == True
    assert Cardinality.ZERO_OR_ONE.is_specified() == True
    assert Cardinality.ZERO_OR_MANY.is_specified() == True

