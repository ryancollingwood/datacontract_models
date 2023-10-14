from models import DataClassification


def test_data_classification_values():
    options = [x.value for x in DataClassification]
    assert options == [
        "UNSPECIFIED",
        "Public",
        "Private",
        "Internal",
        "Confidential",
        "Restricted",
    ]


def test_data_classification_repr():
    assert repr(DataClassification.UNSPECIFIED) == "DataClassification.UNSPECIFIED"
    assert repr(DataClassification.PUBLIC) == "DataClassification.PUBLIC"
    assert repr(DataClassification.PRIVATE) == "DataClassification.PRIVATE"
    assert repr(DataClassification.INTERNAL) == "DataClassification.INTERNAL"
    assert repr(DataClassification.CONFIDENTIAL) == "DataClassification.CONFIDENTIAL"
    assert repr(DataClassification.RESTRICTED) == "DataClassification.RESTRICTED"


def test_data_classification_is_specified():
    assert DataClassification.UNSPECIFIED.is_specified() == False
    assert DataClassification.PUBLIC.is_specified() == True
    assert DataClassification.PRIVATE.is_specified() == True
    assert DataClassification.INTERNAL.is_specified() == True
    assert DataClassification.CONFIDENTIAL.is_specified() == True
    assert DataClassification.RESTRICTED.is_specified() == True
