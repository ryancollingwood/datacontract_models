from models import DatabaseTable
from .test_database import reference_database


reference_database_table = DatabaseTable(
    name="orders",
    database=reference_database,
    )


def test_database_table():
    database_table = DatabaseTable(
        name="orders",
        database=reference_database,
        )
    
    assert database_table.name == "orders"
    assert database_table.database == reference_database


def test_database_table_repr():
    database_table = DatabaseTable(
        name="orders",
        database=reference_database,
        )
    
    assert repr(database_table) == "DatabaseTable(name='orders', database=Database(name='ecommerce'))"


def test_database_table_extra_attributes():
    database_table = DatabaseTable(
        name="orders",
        database=reference_database,
        extra="extra",
        )
    
    assert database_table.extra == "extra"