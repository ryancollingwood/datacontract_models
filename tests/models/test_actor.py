from models import Actor


def test_actor():
    actor = Actor(name="Batman")
    assert actor.name == "Batman"


def test_actor_repr():
    actor = Actor(name="Batman")
    assert repr(actor) == "Actor(name='Batman')"


def test_actor_extra_attributes():
    actor = Actor(name="Batman", extra="extra")
    assert actor.extra == "extra"

