from models import *

semantictype_unique_identifier = SemanticType(
    name="unique identifier",
    classification=DataClassification.UNSPECIFIED,
    variety=Variety.GLOBALLY_UNIQUE,
)
semantictype_person_name = SemanticType(
    name="person name",
    classification=DataClassification.UNSPECIFIED,
    variety=Variety.UNSPECIFIED,
)
semantictype_location = SemanticType(
    name="location",
    classification=DataClassification.UNSPECIFIED,
    variety=Variety.UNSPECIFIED,
)
semantictype_product_name = SemanticType(
    name="product name",
    classification=DataClassification.UNSPECIFIED,
    variety=Variety.UNSPECIFIED,
)
semantictype_product_variation = SemanticType(
    name="product variation",
    classification=DataClassification.UNSPECIFIED,
    variety=Variety.UNSPECIFIED,
)
semantictype_product_quantity = SemanticType(
    name="product quantity",
    classification=DataClassification.UNSPECIFIED,
    variety=Variety.UNSPECIFIED,
)
propertyattribute_id = PropertyAttribute(
    name="id",
    semantic_type=semantictype_unique_identifier,
)
propertyattribute_name = PropertyAttribute(
    name="name",
    semantic_type=semantictype_person_name,
    alias="Customer Name",
)
propertyattribute_address_lines = PropertyAttribute(
    name="address lines",
    semantic_type=semantictype_location,
)
propertyattribute_menu_item = PropertyAttribute(
    name="menu item",
    semantic_type=semantictype_unique_identifier,
)
propertyattribute_menu_description = PropertyAttribute(
    name="menu description",
    semantic_type=semantictype_product_name,
)
propertyattribute_variation = PropertyAttribute(
    name="variation",
    semantic_type=semantictype_product_variation,
    alias="Modifications",
)
propertyattribute_quantity = PropertyAttribute(
    name="quantity",
    semantic_type=semantictype_product_quantity,
)
databasepath_super_pos_customers_id = DatabasePath(
    database="super_pos", table="customers", column="id"
)
databasepath_super_pos_customers_first_name = DatabasePath(
    database="super_pos",
    table="customers",
    column="first_name",
)
databasepath_super_pos_adresses_id = DatabasePath(
    database="super_pos", table="adresses", column="id"
)
databasepath_super_pos_products_id = DatabasePath(
    database="super_pos", table="products", column="id"
)
database_super_pos = Database(name="super_pos")
databasetable_orders = DatabaseTable(name="orders", database=database_super_pos)
databasecolumn_customer_id = DatabaseColumn(
    name="customer_id",
    table=databasetable_orders,
    schema_type=SchemaType.GUID,
    not_null=True,
    is_unique=True,
    references=databasepath_super_pos_customers_id,
)
databasecolumn_customer_first_name = DatabaseColumn(
    name="customer_first_name",
    table=databasetable_orders,
    schema_type=SchemaType.STR,
    not_null=True,
    is_unique=False,
    references=databasepath_super_pos_customers_first_name,
)
databasecolumn_address_id = DatabaseColumn(
    name="address_id",
    table=databasetable_orders,
    schema_type=SchemaType.GUID,
    not_null=True,
    is_unique=False,
    references=databasepath_super_pos_adresses_id,
)
databasecolumn_product_id = DatabaseColumn(
    name="product_id",
    table=databasetable_orders,
    schema_type=SchemaType.GUID,
    not_null=True,
    is_unique=False,
    references=databasepath_super_pos_products_id,
)
databasecolumn_variation = DatabaseColumn(
    name="variation",
    table=databasetable_orders,
    schema_type=SchemaType.STR,
    not_null=False,
    is_unique=False,
    references=None,
)
databasecolumn_quantity = DatabaseColumn(
    name="quantity",
    table=databasetable_orders,
    schema_type=SchemaType.INT,
    not_null=True,
    is_unique=False,
    references=None,
)
aggregate_customer = Aggregate(
    name="customer",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_id,
            source=databasecolumn_customer_id,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_name,
            source=databasecolumn_customer_first_name,
        ),
    ],
)
aggregate_customer_address = Aggregate(
    name="customer address",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_id,
            source=databasecolumn_address_id,
        ),
        Property(
            cardinality=Cardinality.ONE_OR_MORE,
            attribute=propertyattribute_address_lines,
            source=None,
        ),
    ],
)
aggregate_order_items = Aggregate(
    name="order items",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_menu_item,
            source=databasecolumn_product_id,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_menu_description,
            source=None,
        ),
        Property(
            cardinality=Cardinality.ZERO_OR_MANY,
            attribute=propertyattribute_variation,
            source=databasecolumn_variation,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_quantity,
            source=databasecolumn_quantity,
        ),
    ],
)
event_order_requested = Event(
    name="order requested",
    raised_by=Actor(name="customer"),
    received_by=Actor(name="order application"),
    aggregates=[
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=aggregate_customer,
        ),
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=aggregate_customer_address,
        ),
        EventAggregate(
            cardinality=Cardinality.ONE_OR_MORE,
            aggregate=aggregate_order_items,
        ),
    ],
    description="When a customer submits an order before supply payment details",
)

semantictype_currency_aud_excluding_tax = SemanticType(
    name="currency aud excluding tax",
    classification=DataClassification.UNSPECIFIED,
    variety=Variety.UNSPECIFIED,
)
semantictype_currency_aud_including_tax = SemanticType(
    name="currency aud including tax",
    classification=DataClassification.UNSPECIFIED,
    variety=Variety.UNSPECIFIED,
)
propertyattribute_order_id = PropertyAttribute(
    name="order id",
    semantic_type=semantictype_unique_identifier,
)
propertyattribute_order_subtotal = PropertyAttribute(
    name="order subtotal",
    semantic_type=semantictype_currency_aud_excluding_tax,
)
propertyattribute_order_total = PropertyAttribute(
    name="order total",
    semantic_type=semantictype_currency_aud_including_tax,
)
propertyattribute_address_id = PropertyAttribute(
    name="address id",
    semantic_type=semantictype_unique_identifier,
)
propertyattribute_item_price = PropertyAttribute(
    name="item price",
    semantic_type=semantictype_currency_aud_excluding_tax,
)
propertyattribute_line_total = PropertyAttribute(
    name="line total",
    semantic_type=semantictype_currency_aud_excluding_tax,
)
databasecolumn_id = DatabaseColumn(
    name="id",
    table=databasetable_orders,
    schema_type=SchemaType.GUID,
    not_null=True,
    is_unique=True,
    references=None,
)
databasecolumn_subtotal = DatabaseColumn(
    name="subtotal",
    table=databasetable_orders,
    schema_type=SchemaType.DECIMAL,
    not_null=True,
    is_unique=False,
    references=None,
)
databasecolumn_total = DatabaseColumn(
    name="total",
    table=databasetable_orders,
    schema_type=SchemaType.DECIMAL,
    not_null=True,
    is_unique=False,
    references=None,
)
databasecolumn_item_price_aud_ex_tax = DatabaseColumn(
    name="item_price_aud_ex_tax",
    table=databasetable_orders,
    schema_type=SchemaType.DECIMAL,
    not_null=True,
    is_unique=False,
    references=None,
)
databasecolumn_line_total_aud_ex_tax = DatabaseColumn(
    name="line_total_aud_ex_tax",
    table=databasetable_orders,
    schema_type=SchemaType.DECIMAL,
    not_null=True,
    is_unique=False,
    references=None,
)
aggregate_order = Aggregate(
    name="order",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_order_id,
            source=databasecolumn_id,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_order_subtotal,
            source=databasecolumn_subtotal,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_order_total,
            source=databasecolumn_total,
        ),
    ],
)
order_confirmed_customer = Aggregate(
    name="customer",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_id,
            source=databasecolumn_customer_id,
        )
    ],
)
order_confirmed_customer_address = Aggregate(
    name="customer address",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_address_id,
            source=databasecolumn_address_id,
        )
    ],
)
order_confirmed_order_items = Aggregate(
    name="order items",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_menu_item,
            source=databasecolumn_product_id,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_menu_description,
            source=None,
        ),
        Property(
            cardinality=Cardinality.ZERO_OR_MANY,
            attribute=propertyattribute_variation,
            source=databasecolumn_variation,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_quantity,
            source=databasecolumn_quantity,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_item_price,
            source=databasecolumn_item_price_aud_ex_tax,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_line_total,
            source=databasecolumn_line_total_aud_ex_tax,
        ),
    ],
)
event_order_confirmed = Event(
    name="order confirmed",
    raised_by=Actor(name="order application"),
    received_by=Actor(name="customer"),
    aggregates=[
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=aggregate_order,
        ),
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=order_confirmed_customer,
        ),
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=order_confirmed_customer_address,
        ),
        EventAggregate(
            cardinality=Cardinality.ONE_OR_MORE,
            aggregate=order_confirmed_order_items,
        ),
    ],
    description="Once payment has been received and all validations of the customer details have been completed",
)

databasetable_adresses = DatabaseTable(name="adresses", database=database_super_pos)
customer_details_updated_current_address_id = DatabaseColumn(
    name="id",
    table=databasetable_adresses,
    schema_type=SchemaType.GUID,
    not_null=True,
    is_unique=True,
    references=databasepath_super_pos_adresses_id,
)
databasecolumn_line_ = DatabaseColumn(
    name="line_1",
    table=databasetable_adresses,
    schema_type=SchemaType.STR,
    not_null=True,
    is_unique=False,
    references=None,
)
aggregate_current_address = Aggregate(
    name="current address",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_id,
            source=customer_details_updated_current_address_id,
        ),
        Property(
            cardinality=Cardinality.ONE_OR_MORE,
            attribute=propertyattribute_address_lines,
            source=databasecolumn_line_,
        ),
    ],
)
aggregate_prioir_addresses = Aggregate(
    name="prioir addresses",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_id,
            source=customer_details_updated_current_address_id,
        ),
        Property(
            cardinality=Cardinality.ONE_OR_MORE,
            attribute=propertyattribute_address_lines,
            source=databasecolumn_line_,
        ),
    ],
)
event_customer_details_updated = Event(
    name="customer details updated",
    raised_by=Actor(name="customer"),
    received_by=Actor(name="order application"),
    aggregates=[
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=aggregate_customer,
        ),
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=aggregate_current_address,
        ),
        EventAggregate(
            cardinality=Cardinality.ZERO_OR_MANY,
            aggregate=aggregate_prioir_addresses,
        ),
    ],
    description="When a customer updates their details",
)
