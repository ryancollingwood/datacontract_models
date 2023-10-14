from models import Aggregate

from .test_property import reference_property


reference_aggregate = Aggregate(
    name="Sales",
    properties=[
        reference_property,
    ]
)


def test_aggregate():
    aggregate = Aggregate(
        name="Sales",
        properties=[
            reference_property,
        ]
    )
    assert aggregate.name == "Sales"
    assert aggregate.properties[0].name() == "Invoice Total"

