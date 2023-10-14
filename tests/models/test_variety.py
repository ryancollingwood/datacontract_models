from models import Variety


def test_variety_values():
    options = [x.value for x in Variety]
    assert options == [
        "UNSPECIFIED",
        "Variable",
        "LimitedSubset",
        "LocallyUnique",
        "GloballyUnique",
    ]


def test_variety_is_unique():
    assert Variety.UNSPECIFIED.is_unique() == False
    assert Variety.VARIABLE.is_unique() == False
    assert Variety.LIMITED_SUBSET.is_unique() == False
    assert Variety.LOCALLY_UNIQUE.is_unique() == True
    assert Variety.GLOBALLY_UNIQUE.is_unique() == True


def test_variety_reper():
    assert repr(Variety.UNSPECIFIED) == "Variety.UNSPECIFIED"
    assert repr(Variety.VARIABLE) == "Variety.VARIABLE"
    assert repr(Variety.LIMITED_SUBSET) == "Variety.LIMITED_SUBSET"
    assert repr(Variety.LOCALLY_UNIQUE) == "Variety.LOCALLY_UNIQUE"
    assert repr(Variety.GLOBALLY_UNIQUE) == "Variety.GLOBALLY_UNIQUE"


def test_variety_is_specified():
    assert Variety.UNSPECIFIED.is_specified() == False
    assert Variety.VARIABLE.is_specified() == True
    assert Variety.LIMITED_SUBSET.is_specified() == True
    assert Variety.LOCALLY_UNIQUE.is_specified() == True
    assert Variety.GLOBALLY_UNIQUE.is_specified() == True
