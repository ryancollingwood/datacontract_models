from models import EventAggregate, Cardinality
from .test_aggregate import reference_aggregate

def test_event_aggregate():
    event_aggregate = EventAggregate(
        aggregate=reference_aggregate,
        cardinality=Cardinality.ONLY_ONE,
    )