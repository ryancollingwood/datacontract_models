from models import Database


reference_database = Database(name="ecommerce")


def test_database():
    database = Database(name="ecommerce")
    assert database.name == "ecommerce"


def test_database_repr():
    database = Database(name="ecommerce")
    assert repr(database) == "Database(name='ecommerce')"


def test_database_extra_attributes():
    database = Database(name="ecommerce", extra="extra")
    assert database.extra == "extra"


def test_database_to_contract():
    database = Database(name="ecommerce", extra="extra")
    assert database.to_contract() == {"name": "ecommerce", "extra": "extra"}

