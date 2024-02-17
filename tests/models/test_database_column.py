from models import DatabaseColumn, SchemaType
from .test_database_table import reference_database_table
from .test_database_path import reference_database_path


reference_database_column = DatabaseColumn(
        name="order_id",
        table=reference_database_table,
        schema_type=SchemaType.UUID,
        not_null=False,
        is_unique=True,
    )

boolean_database_column = DatabaseColumn(
    name = "is_active",
    table=reference_database_table,
    schema_type=SchemaType.BOOLEAN,
    not_null=True,
    is_unique=False,
)


def test_database_column():
    database_column = DatabaseColumn(
        name="order_id",
        table=reference_database_table,
        schema_type=SchemaType.UUID,
        not_null=False,
        is_unique=True,
    )

    assert database_column.name == "order_id"
    assert database_column.table == reference_database_table
    assert database_column.schema_type == SchemaType.UUID
    assert database_column.not_null is False
    assert database_column.is_unique is True


def test_database_column_repr():
    database_column = DatabaseColumn(
        name="order_id",
        table=reference_database_table,
        schema_type=SchemaType.UUID,
        not_null=False,
        is_unique=True,
    )

    assert (
        repr(database_column)
        == "DatabaseColumn(name='order_id', table=DatabaseTable(name='orders', database=Database(name='ecommerce')), schema_type=SchemaType.UUID, not_null=False, is_unique=True, references=None)"
    )


def test_database_column_extra_attributes():
    database_column = DatabaseColumn(
        name="order_id",
        table=reference_database_table,
        schema_type=SchemaType.UUID,
        not_null=False,
        is_unique=True,
        extra="extra",
    )

    assert database_column.extra == "extra"


def test_database_column_with_path():
    database_column = DatabaseColumn(
        name="order_id",
        table=reference_database_table,
        schema_type=SchemaType.UUID,
        not_null=False,
        is_unique=True,
        references=reference_database_path,
    )

    assert database_column.references == reference_database_path


def test_database_column_with_path_to_contract():
    database_column = DatabaseColumn(
        name="order_id",
        table=reference_database_table,
        schema_type=SchemaType.UUID,
        not_null=False,
        is_unique=True,
        references=reference_database_path,
    )

    assert database_column.to_contract() == {
        "database": "ecommerce",
        "table": "orders",
        "column": "order_id",
        "schema_type": "uuid",
        "not_null": False,
        "is_unique": True,
        "references": {
            'column': 'order_id',
            'database': 'ecommerce',
            'table': 'orders',
        },
    }

