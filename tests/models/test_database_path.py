from models import DatabasePath, DatabaseColumn, DatabaseTable, Database, SchemaType


reference_database_path = DatabasePath(
    database="ecommerce",
    table="orders",
    column="order_id",
)


def test_database_path():
    database_path = DatabasePath(
        database="ecommerce",
        table="orders",
        column="order_id",
    )

    assert database_path.database == "ecommerce"
    assert database_path.table == "orders"
    assert database_path.column == "order_id"


def test_database_path_name():
    database_path = DatabasePath(
        database="ecommerce",
        table="orders",
        column="order_id",
    )

    assert database_path.name == "ecommerce.orders.order_id"


def test_database_path_repr():
    database_path = DatabasePath(
        database="ecommerce",
        table="orders",
        column="order_id",
    )

    assert (
        repr(database_path)
        == "DatabasePath(database='ecommerce', table='orders', column='order_id')"
    )


def test_database_path_extra_attributes():
    database_path = DatabasePath(
        database="ecommerce", table="orders", column="order_id", extra="extra"
    )

    assert database_path.extra == "extra"


def test_database_path_to_contract():
    database_path = DatabasePath(
        database="ecommerce", table="orders", column="order_id", extra="extra"
    )

    assert database_path.to_contract() == {
        "database": "ecommerce",
        "table": "orders",
        "column": "order_id",
        "extra": "extra",
    }


def test_database_path_from_database_column():
    db_col = DatabaseColumn(
        name="order_id",
        table=DatabaseTable(
            name="orders",
            database=Database(name="ecommerce"),
        ),
        schema_type=SchemaType.UUID,
        not_null=False,
        is_unique=True,
        references=None,
    )

    database_path = DatabasePath.from_database_column(db_col)

    assert database_path.database == "ecommerce"
    assert database_path.table == "orders"
    assert database_path.column == "order_id"
    assert database_path.name == "ecommerce.orders.order_id"

