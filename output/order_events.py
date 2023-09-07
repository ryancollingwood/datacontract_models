from models import *

event_order_requested = Event(
    name="order requested",
    raised_by=Actor(name="customer"),
    received_by=Actor(name="order application"),
    aggregates=[
        EventAggregate(
            name="customer",
            aggregate=Aggregate(
                name="customer",
                properties=[
                    Property(
                        name="id",
                        attribute=PropertyAttribute(
                            name="id",
                            semantic_type=SemanticType(name="unique identifier"),
                        ),
                        source=DatabaseColumn(
                            name="customer_id",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.GUID,
                            not_null=True,
                            is_unique=True,
                            references=None,
                        ),
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    ),
                    Property(
                        name="name",
                        attribute=PropertyAttribute(
                            name="name", semantic_type=SemanticType(name="person name")
                        ),
                        source=DatabaseColumn(
                            name="customer_first_name",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.STR,
                            not_null=True,
                            is_unique=False,
                            references=None,
                        ),
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    ),
                ],
            ),
            cardinality=Cardinality.ONLY_ONE,
        ),
        EventAggregate(
            name="customer address",
            aggregate=Aggregate(
                name="customer address",
                properties=[
                    Property(
                        name="id",
                        attribute=PropertyAttribute(
                            name="id",
                            semantic_type=SemanticType(name="unique identifier"),
                        ),
                        source=DatabaseColumn(
                            name="address_id",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.GUID,
                            not_null=True,
                            is_unique=False,
                            references=None,
                        ),
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    ),
                    Property(
                        name="address lines",
                        attribute=PropertyAttribute(
                            name="address lines",
                            semantic_type=SemanticType(name="location"),
                        ),
                        source=None,
                        cardinality=Cardinality.ONE_OR_MORE,
                        is_identifier=False,
                    ),
                ],
            ),
            cardinality=Cardinality.ONLY_ONE,
        ),
        EventAggregate(
            name="order items",
            aggregate=Aggregate(
                name="order items",
                properties=[
                    Property(
                        name="menu item",
                        attribute=PropertyAttribute(
                            name="menu item",
                            semantic_type=SemanticType(name="unique identifier"),
                        ),
                        source=DatabaseColumn(
                            name="product_id",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.GUID,
                            not_null=True,
                            is_unique=False,
                            references=None,
                        ),
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    ),
                    Property(
                        name="menu description",
                        attribute=PropertyAttribute(
                            name="menu description",
                            semantic_type=SemanticType(name="product name"),
                        ),
                        source=None,
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    ),
                    Property(
                        name="variation",
                        attribute=PropertyAttribute(
                            name="variation",
                            semantic_type=SemanticType(name="product variation"),
                        ),
                        source=DatabaseColumn(
                            name="variation",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.STR,
                            not_null=False,
                            is_unique=False,
                            references=None,
                        ),
                        cardinality=Cardinality.ZERO_OR_MANY,
                        is_identifier=False,
                    ),
                    Property(
                        name="quantity",
                        attribute=PropertyAttribute(
                            name="quantity",
                            semantic_type=SemanticType(name="product quantity"),
                        ),
                        source=DatabaseColumn(
                            name="quantity",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.INT,
                            not_null=True,
                            is_unique=False,
                            references=None,
                        ),
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    ),
                ],
            ),
            cardinality=Cardinality.ONE_OR_MORE,
        ),
    ],
)

event_order_confirmed = Event(
    name="order confirmed",
    raised_by=Actor(name="order application"),
    received_by=Actor(name="customer"),
    aggregates=[
        EventAggregate(
            name="order",
            aggregate=Aggregate(
                name="order",
                properties=[
                    Property(
                        name="order id",
                        attribute=PropertyAttribute(
                            name="order id",
                            semantic_type=SemanticType(name="unique identifier"),
                        ),
                        source=DatabaseColumn(
                            name="id",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.GUID,
                            not_null=True,
                            is_unique=True,
                            references=None,
                        ),
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    ),
                    Property(
                        name="order subtotal",
                        attribute=PropertyAttribute(
                            name="order subtotal",
                            semantic_type=SemanticType(
                                name="currency aud excluding tax"
                            ),
                        ),
                        source=DatabaseColumn(
                            name="subtotal",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.DECIMAL,
                            not_null=True,
                            is_unique=False,
                            references=None,
                        ),
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    ),
                    Property(
                        name="order total",
                        attribute=PropertyAttribute(
                            name="order total",
                            semantic_type=SemanticType(
                                name="currency aud including tax"
                            ),
                        ),
                        source=DatabaseColumn(
                            name="total",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.DECIMAL,
                            not_null=True,
                            is_unique=False,
                            references=None,
                        ),
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    ),
                ],
            ),
            cardinality=Cardinality.ONLY_ONE,
        ),
        EventAggregate(
            name="customer",
            aggregate=Aggregate(
                name="customer",
                properties=[
                    Property(
                        name="id",
                        attribute=PropertyAttribute(
                            name="id",
                            semantic_type=SemanticType(name="unique identifier"),
                        ),
                        source=DatabaseColumn(
                            name="customer_id",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.GUID,
                            not_null=True,
                            is_unique=True,
                            references=None,
                        ),
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    )
                ],
            ),
            cardinality=Cardinality.ONLY_ONE,
        ),
        EventAggregate(
            name="customer address",
            aggregate=Aggregate(
                name="customer address",
                properties=[
                    Property(
                        name="address id",
                        attribute=PropertyAttribute(
                            name="address id",
                            semantic_type=SemanticType(name="unique identifier"),
                        ),
                        source=DatabaseColumn(
                            name="address_id",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.GUID,
                            not_null=True,
                            is_unique=False,
                            references=None,
                        ),
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    )
                ],
            ),
            cardinality=Cardinality.ONLY_ONE,
        ),
        EventAggregate(
            name="order items",
            aggregate=Aggregate(
                name="order items",
                properties=[
                    Property(
                        name="menu item",
                        attribute=PropertyAttribute(
                            name="menu item",
                            semantic_type=SemanticType(name="unique identifier"),
                        ),
                        source=DatabaseColumn(
                            name="product_id",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.GUID,
                            not_null=True,
                            is_unique=False,
                            references=None,
                        ),
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    ),
                    Property(
                        name="menu description",
                        attribute=PropertyAttribute(
                            name="menu description",
                            semantic_type=SemanticType(name="product name"),
                        ),
                        source=None,
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    ),
                    Property(
                        name="variation",
                        attribute=PropertyAttribute(
                            name="variation",
                            semantic_type=SemanticType(name="product variation"),
                        ),
                        source=DatabaseColumn(
                            name="variation",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.STR,
                            not_null=False,
                            is_unique=False,
                            references=None,
                        ),
                        cardinality=Cardinality.ZERO_OR_MANY,
                        is_identifier=False,
                    ),
                    Property(
                        name="quantity",
                        attribute=PropertyAttribute(
                            name="quantity",
                            semantic_type=SemanticType(name="product quantity"),
                        ),
                        source=DatabaseColumn(
                            name="quantity",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.INT,
                            not_null=True,
                            is_unique=False,
                            references=None,
                        ),
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    ),
                    Property(
                        name="item price",
                        attribute=PropertyAttribute(
                            name="item price",
                            semantic_type=SemanticType(
                                name="currency aud excluding tax"
                            ),
                        ),
                        source=DatabaseColumn(
                            name="item_price_aud_ex_tax",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.DECIMAL,
                            not_null=True,
                            is_unique=False,
                            references=None,
                        ),
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    ),
                    Property(
                        name="line total",
                        attribute=PropertyAttribute(
                            name="line total",
                            semantic_type=SemanticType(
                                name="currency aud excluding tax"
                            ),
                        ),
                        source=DatabaseColumn(
                            name="line_total_aud_ex_tax",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.DECIMAL,
                            not_null=True,
                            is_unique=False,
                            references=None,
                        ),
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    ),
                ],
            ),
            cardinality=Cardinality.ONE_OR_MORE,
        ),
    ],
)

event_customer_details_updated = Event(
    name="customer details updated",
    raised_by=Actor(name="customer"),
    received_by=Actor(name="order application"),
    aggregates=[
        EventAggregate(
            name="customer",
            aggregate=Aggregate(
                name="customer",
                properties=[
                    Property(
                        name="id",
                        attribute=PropertyAttribute(
                            name="id",
                            semantic_type=SemanticType(name="unique identifier"),
                        ),
                        source=DatabaseColumn(
                            name="customer_id",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.GUID,
                            not_null=True,
                            is_unique=True,
                            references=None,
                        ),
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    ),
                    Property(
                        name="name",
                        attribute=PropertyAttribute(
                            name="name", semantic_type=SemanticType(name="person name")
                        ),
                        source=DatabaseColumn(
                            name="customer_first_name",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.STR,
                            not_null=True,
                            is_unique=False,
                            references=None,
                        ),
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    ),
                ],
            ),
            cardinality=Cardinality.ONLY_ONE,
        ),
        EventAggregate(
            name="current address",
            aggregate=Aggregate(
                name="current address",
                properties=[
                    Property(
                        name="id",
                        attribute=PropertyAttribute(
                            name="id",
                            semantic_type=SemanticType(name="unique identifier"),
                        ),
                        source=DatabaseColumn(
                            name="id",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.GUID,
                            not_null=True,
                            is_unique=True,
                            references=None,
                        ),
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    ),
                    Property(
                        name="address lines",
                        attribute=PropertyAttribute(
                            name="address lines",
                            semantic_type=SemanticType(name="location"),
                        ),
                        source=DatabaseColumn(
                            name="line_1",
                            table=DatabaseTable(
                                name="adresses", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.STR,
                            not_null=True,
                            is_unique=False,
                            references=None,
                        ),
                        cardinality=Cardinality.ONE_OR_MORE,
                        is_identifier=False,
                    ),
                ],
            ),
            cardinality=Cardinality.ONLY_ONE,
        ),
        EventAggregate(
            name="prioir addresses",
            aggregate=Aggregate(
                name="prioir addresses",
                properties=[
                    Property(
                        name="id",
                        attribute=PropertyAttribute(
                            name="id",
                            semantic_type=SemanticType(name="unique identifier"),
                        ),
                        source=DatabaseColumn(
                            name="id",
                            table=DatabaseTable(
                                name="orders", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.GUID,
                            not_null=True,
                            is_unique=True,
                            references=None,
                        ),
                        cardinality=Cardinality.ONLY_ONE,
                        is_identifier=False,
                    ),
                    Property(
                        name="address lines",
                        attribute=PropertyAttribute(
                            name="address lines",
                            semantic_type=SemanticType(name="location"),
                        ),
                        source=DatabaseColumn(
                            name="line_1",
                            table=DatabaseTable(
                                name="adresses", database=Database(name="super_pos")
                            ),
                            schema_type=SchemaType.STR,
                            not_null=True,
                            is_unique=False,
                            references=None,
                        ),
                        cardinality=Cardinality.ONE_OR_MORE,
                        is_identifier=False,
                    ),
                ],
            ),
            cardinality=Cardinality.ZERO_OR_MANY,
        ),
    ],
)
