from models import *

actor_customer = Actor(name="Customer")
actor_identity_service = Actor(name="Identity Service")
semantictype_user_id = SemanticType(
    name="User ID",
    classification=DataClassification.INTERNAL,
    variety=Variety.GLOBALLY_UNIQUE,
)
semantictype_date = SemanticType(
    name="Date",
    classification=DataClassification.INTERNAL,
    variety=Variety.VARIABLE,
)
semantictype_identity_provider = SemanticType(
    name="Identity Provider",
    classification=DataClassification.INTERNAL,
    variety=Variety.LIMITED_SUBSET,
)
semantictype_permission = SemanticType(
    name="Permission",
    classification=DataClassification.CONFIDENTIAL,
    variety=Variety.LIMITED_SUBSET,
)
semantictype_referral_status = SemanticType(
    name="Referral Status",
    classification=DataClassification.INTERNAL,
    variety=Variety.LIMITED_SUBSET,
)
semantictype_payment_method = SemanticType(
    name="Payment Method",
    classification=DataClassification.RESTRICTED,
    variety=Variety.LIMITED_SUBSET,
)
propertyattribute_user_id = PropertyAttribute(
    name="User ID",
    semantic_type=semantictype_user_id,
    alias="Unique User ID",
)
propertyattribute_registration_date = PropertyAttribute(
    name="Registration Date",
    semantic_type=semantictype_date,
)
propertyattribute_registration_method = PropertyAttribute(
    name="Registration Method",
    semantic_type=semantictype_identity_provider,
)
propertyattribute_enabled_permissions = PropertyAttribute(
    name="Enabled Permissions",
    semantic_type=semantictype_permission,
)
propertyattribute_referred = PropertyAttribute(
    name="Referred",
    semantic_type=semantictype_referral_status,
)
propertyattribute_payment_methods_added = PropertyAttribute(
    name="Payment Methods Added",
    semantic_type=semantictype_payment_method,
)
propertyattribute_login_method = PropertyAttribute(
    name="Login Method",
    semantic_type=semantictype_identity_provider,
)
databasepath_ecommerce_users_id = DatabasePath(
    database="ecommerce", table="users", column="id"
)
databasepath_ecommerce_login_providers_id = DatabasePath(
    database="ecommerce",
    table="login_providers",
    column="id",
)
databasepath_ecommerce_permissions_id = DatabasePath(
    database="ecommerce", table="permissions", column="id"
)
databasepath_ecommerce_payment_methods_id = DatabasePath(
    database="ecommerce",
    table="payment_methods",
    column="id",
)
database_ecommerce = Database(name="ecommerce")
databasetable_registrations = DatabaseTable(
    name="registrations",
    database=database_ecommerce,
)
databasecolumn_user_id = DatabaseColumn(
    name="user_id",
    table=databasetable_registrations,
    schema_type=SchemaType.STR,
    not_null=True,
    is_unique=True,
    references=databasepath_ecommerce_users_id,
)
databasecolumn_registered_at = DatabaseColumn(
    name="registered_at",
    table=databasetable_registrations,
    schema_type=SchemaType.DATE,
    not_null=True,
    is_unique=False,
    references=None,
)
databasecolumn_registration_provider_id = DatabaseColumn(
    name="registration_provider_id",
    table=databasetable_registrations,
    schema_type=SchemaType.STR,
    not_null=True,
    is_unique=False,
    references=databasepath_ecommerce_login_providers_id,
)
databasecolumn_granted_permissions = DatabaseColumn(
    name="granted_permissions",
    table=databasetable_registrations,
    schema_type=SchemaType.STR,
    not_null=False,
    is_unique=False,
    references=databasepath_ecommerce_permissions_id,
)
databasecolumn_is_referral = DatabaseColumn(
    name="is_referral",
    table=databasetable_registrations,
    schema_type=SchemaType.BOOLEAN,
    not_null=True,
    is_unique=False,
    references=None,
)
databasecolumn_payment_methods = DatabaseColumn(
    name="payment_methods",
    table=databasetable_registrations,
    schema_type=SchemaType.STR,
    not_null=False,
    is_unique=False,
    references=databasepath_ecommerce_payment_methods_id,
)
databasecolumn_login_provider_id = DatabaseColumn(
    name="login_provider_id",
    table=databasetable_registrations,
    schema_type=SchemaType.STR,
    not_null=True,
    is_unique=False,
    references=databasepath_ecommerce_login_providers_id,
)
aggregate_user_registration = Aggregate(
    name="User Registration",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_user_id,
            source=databasecolumn_user_id,
            timing=None,
            type="User Property",
            sample_values="c81159b1-2658-5fba-b59b-16a0d4e30217",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_registration_date,
            source=databasecolumn_registered_at,
            timing=MetaTiming.UNSPECIFIED,
            type="User Property",
            sample_values="YYYY-MM-DDTHH:MM:SS",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_registration_method,
            source=databasecolumn_registration_provider_id,
            timing=None,
            type="User Property",
            sample_values="Google, Facebook, E-mail",
        ),
    ],
)
aggregate_user_profile = Aggregate(
    name="User Profile",
    properties=[
        Property(
            cardinality=Cardinality.ZERO_OR_MANY,
            attribute=propertyattribute_enabled_permissions,
            source=databasecolumn_granted_permissions,
            timing=None,
            type="User Property",
            sample_values='["Touch ID", "Face ID"]',
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_referred,
            source=databasecolumn_is_referral,
            timing=None,
            type="User Property",
            sample_values=True,
        ),
        Property(
            cardinality=Cardinality.ZERO_OR_MANY,
            attribute=propertyattribute_payment_methods_added,
            source=databasecolumn_payment_methods,
            timing=None,
            type="User Property",
            sample_values='["Credit", "Debit"]',
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_login_method,
            source=databasecolumn_login_provider_id,
            timing=None,
            type="Event Property",
            sample_values="Email, Facebook, Google",
        ),
    ],
)
event_sign_up_completed = Event(
    name="Sign Up Completed",
    raised_by=actor_customer,
    received_by=actor_identity_service,
    aggregates=[
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=aggregate_user_registration,
        ),
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=aggregate_user_profile,
        ),
    ],
    description="User successfully signs up",
    kpi="First Purchase Completed within 7 Days of Account Creation",
)

databasetable_sessions = DatabaseTable(name="sessions", database=database_ecommerce)
login_completed_user_session_user_id = DatabaseColumn(
    name="user_id",
    table=databasetable_sessions,
    schema_type=SchemaType.STR,
    not_null=True,
    is_unique=False,
    references=databasepath_ecommerce_users_id,
)
aggregate_user_session = Aggregate(
    name="User Session",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_user_id,
            source=login_completed_user_session_user_id,
            timing=None,
            type="User Property",
            sample_values="c81159b1-2658-5fba-b59b-16a0d4e30217",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_login_method,
            source=databasecolumn_login_provider_id,
            timing=None,
            type="Event Property",
            sample_values="Email, Facebook, Google",
        ),
    ],
)
event_login_completed = Event(
    name="Login Completed",
    raised_by=actor_customer,
    received_by=actor_identity_service,
    aggregates=[
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=aggregate_user_session,
        )
    ],
    description="User successfully logs in",
    kpi="First Purchase Completed within 7 Days of Account Creation",
)

actor_search_service = Actor(name="Search Service")
event_searched_from_home_page = Event(
    name="Searched from Home Page",
    raised_by=actor_customer,
    received_by=actor_search_service,
    aggregates=[],
    description="User completes a search from the home page",
    kpi="First Purchase Completed within 7 Days of Account Creation",
)

event_searched_from_banners = Event(
    name="Searched from Banners",
    raised_by=actor_customer,
    received_by=actor_search_service,
    aggregates=[],
    description="User completes a search from banners",
    kpi="First Purchase Completed within 7 Days of Account Creation",
)

semantictype_item_attribute = SemanticType(
    name="Item Attribute",
    classification=DataClassification.INTERNAL,
    variety=Variety.VARIABLE,
)
semantictype_item_attribute_value = SemanticType(
    name="Item Attribute Value",
    classification=DataClassification.INTERNAL,
    variety=Variety.VARIABLE,
)
semantictype_whole_number = SemanticType(
    name="Whole Number",
    classification=DataClassification.INTERNAL,
    variety=Variety.VARIABLE,
)
propertyattribute_filter_category = PropertyAttribute(
    name="Filter Category",
    semantic_type=semantictype_item_attribute,
)
propertyattribute_filter_option_selected = PropertyAttribute(
    name="Filter Option Selected",
    semantic_type=semantictype_item_attribute_value,
)
propertyattribute_of_results = PropertyAttribute(
    name="# of Results",
    semantic_type=semantictype_whole_number,
)
database_user_search = Database(name="user_search")
databasetable_session_filters = DatabaseTable(
    name="session_filters",
    database=database_user_search,
)
databasecolumn_filter_category = DatabaseColumn(
    name="filter_category",
    table=databasetable_session_filters,
    schema_type=SchemaType.STR,
    not_null=True,
    is_unique=False,
    references=None,
)
databasecolumn_is_suggestion = DatabaseColumn(
    name="is_suggestion",
    table=databasetable_session_filters,
    schema_type=SchemaType.STR,
    not_null=True,
    is_unique=False,
    references=None,
)
databasecolumn_total_results = DatabaseColumn(
    name="total_results",
    table=databasetable_session_filters,
    schema_type=SchemaType.INT,
    not_null=True,
    is_unique=False,
    references=None,
)
aggregate_item_search = Aggregate(
    name="Item Search",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_filter_category,
            source=databasecolumn_filter_category,
            timing=None,
            type="Event Property",
            sample_values="Color",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_filter_option_selected,
            source=databasecolumn_is_suggestion,
            timing=None,
            type="Event Property",
            sample_values="Pink, Blue",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_of_results,
            source=databasecolumn_total_results,
            timing=None,
            type="Event Property",
            sample_values=15,
        ),
    ],
)
event_search_filtered = Event(
    name="Search Filtered",
    raised_by=actor_customer,
    received_by=actor_search_service,
    aggregates=[
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=aggregate_item_search,
        )
    ],
    description="User filters their search results",
    kpi="First Purchase Completed within 7 Days of Account Creation",
)

actor_product_details_service = Actor(name="Product Details Service")
semantictype_item_id = SemanticType(
    name="Item ID",
    classification=DataClassification.INTERNAL,
    variety=Variety.LOCALLY_UNIQUE,
)
semantictype_money = SemanticType(
    name="Money",
    classification=DataClassification.INTERNAL,
    variety=Variety.VARIABLE,
)
semantictype_item_name = SemanticType(
    name="Item Name",
    classification=DataClassification.INTERNAL,
    variety=Variety.VARIABLE,
)
semantictype_item_type = SemanticType(
    name="Item Type",
    classification=DataClassification.INTERNAL,
    variety=Variety.VARIABLE,
)
semantictype_currency = SemanticType(
    name="Currency",
    classification=DataClassification.INTERNAL,
    variety=Variety.LIMITED_SUBSET,
)
propertyattribute_item_id = PropertyAttribute(
    name="Item ID",
    semantic_type=semantictype_item_id,
)
propertyattribute_price = PropertyAttribute(
    name="Price",
    semantic_type=semantictype_money,
)
propertyattribute_item_name = PropertyAttribute(
    name="Item Name",
    semantic_type=semantictype_item_name,
)
propertyattribute_item_type = PropertyAttribute(
    name="Item Type",
    semantic_type=semantictype_item_type,
)
propertyattribute_currency = PropertyAttribute(
    name="Currency",
    semantic_type=semantictype_currency,
)
databasepath_pim_products_id = DatabasePath(
    database="pim", table="products", column="id"
)
database_event_stream = Database(name="event_stream")
databasetable_pdp_impressions = DatabaseTable(
    name="pdp_impressions",
    database=database_event_stream,
)
databasecolumn_item_id = DatabaseColumn(
    name="item_id",
    table=databasetable_pdp_impressions,
    schema_type=SchemaType.STR,
    not_null=True,
    is_unique=False,
    references=databasepath_pim_products_id,
)
databasecolumn_price = DatabaseColumn(
    name="price",
    table=databasetable_pdp_impressions,
    schema_type=SchemaType.DECIMAL,
    not_null=True,
    is_unique=False,
    references=None,
)
databasecolumn_item_name = DatabaseColumn(
    name="item_name",
    table=databasetable_pdp_impressions,
    schema_type=SchemaType.STR,
    not_null=True,
    is_unique=False,
    references=None,
)
databasecolumn_item_type = DatabaseColumn(
    name="item_type",
    table=databasetable_pdp_impressions,
    schema_type=SchemaType.STR,
    not_null=True,
    is_unique=False,
    references=None,
)
databasecolumn_currency = DatabaseColumn(
    name="currency",
    table=databasetable_pdp_impressions,
    schema_type=SchemaType.STR,
    not_null=True,
    is_unique=False,
    references=None,
)
aggregate_product_details = Aggregate(
    name="Product Details",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_item_id,
            source=databasecolumn_item_id,
            timing=None,
            type="Event Property",
            sample_values=123456,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_price,
            source=databasecolumn_price,
            timing=None,
            type="Event Property",
            sample_values=5.99,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_item_name,
            source=databasecolumn_item_name,
            timing=None,
            type="Event Property",
            sample_values="Classic Low-Rise",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_item_type,
            source=databasecolumn_item_type,
            timing=None,
            type="Event Property",
            sample_values="Pants",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_currency,
            source=databasecolumn_currency,
            timing=None,
            type="Event Property",
            sample_values="USD, CAN",
        ),
    ],
)
event_item_detail_page_viewed = Event(
    name="Item Detail Page Viewed",
    raised_by=actor_customer,
    received_by=actor_product_details_service,
    aggregates=[
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=aggregate_product_details,
        )
    ],
    description="User views an item detail page",
    kpi="First Purchase Completed within 7 Days of Account Creation",
)

actor_cart_service = Actor(name="Cart Service")
semantictype_boolean = SemanticType(
    name="Boolean",
    classification=DataClassification.INTERNAL,
    variety=Variety.LIMITED_SUBSET,
)
propertyattribute_quick_add_selected = PropertyAttribute(
    name="Quick Add Selected",
    semantic_type=semantictype_boolean,
)
propertyattribute_quantity = PropertyAttribute(
    name="Quantity",
    semantic_type=semantictype_whole_number,
)
aggregate_shopping_cart_line = Aggregate(
    name="Shopping Cart Line",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_item_id,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=123456,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_price,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=5.99,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_item_name,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="Classic Low-Rise",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_item_type,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="Pants",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_quick_add_selected,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=True,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_quantity,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=2,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_currency,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="USD, CAN",
        ),
    ],
)
event_item_added_to_cart = Event(
    name="Item Added to Cart",
    raised_by=actor_customer,
    received_by=actor_cart_service,
    aggregates=[
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=aggregate_shopping_cart_line,
        )
    ],
    description="User adds an item to cart",
    kpi="First Purchase Completed within 7 Days of Account Creation",
)

propertyattribute_of_items_in_cart = PropertyAttribute(
    name="# of Items in Cart",
    semantic_type=semantictype_whole_number,
)
propertyattribute_order_total = PropertyAttribute(
    name="Order Total",
    semantic_type=semantictype_money,
)
propertyattribute_estimated_shipping = PropertyAttribute(
    name="Estimated Shipping",
    semantic_type=semantictype_money,
)
propertyattribute_estimated_tax = PropertyAttribute(
    name="Estimated Tax",
    semantic_type=semantictype_money,
)
propertyattribute_subtotal = PropertyAttribute(
    name="Subtotal",
    semantic_type=semantictype_money,
)
aggregate_shopping_cart = Aggregate(
    name="Shopping Cart",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_of_items_in_cart,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=3,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_order_total,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=19.99,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_estimated_shipping,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=3.99,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_estimated_tax,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=2.5,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_subtotal,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=16.99,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_currency,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="USD, CAN",
        ),
    ],
)
event_cart_viewed = Event(
    name="Cart Viewed",
    raised_by=actor_customer,
    received_by=actor_cart_service,
    aggregates=[
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=aggregate_shopping_cart,
        )
    ],
    description="User views their cart",
    kpi="First Purchase Completed within 7 Days of Account Creation",
)

item_removed_from_cart_shopping_cart_line = Aggregate(
    name="Shopping Cart Line",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_item_id,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=123456,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_item_name,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="Classic",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_item_type,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="Socks",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_price,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=5.99,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_quantity,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=2,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_currency,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="USD, CAN",
        ),
    ],
)
event_item_removed_from_cart = Event(
    name="Item Removed from Cart",
    raised_by=actor_customer,
    received_by=actor_cart_service,
    aggregates=[
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=item_removed_from_cart_shopping_cart_line,
        )
    ],
    description="User removes an item from their cart",
    kpi="# of items removed from cart/WAB",
)

actor_checkout_service = Actor(name="Checkout Service")
view_checkout_shopping_cart_line = Aggregate(
    name="Shopping Cart Line",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_item_id,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=123456,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_price,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=5.99,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_item_name,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="Classic Low-Rise",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_item_type,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="Pants",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_quantity,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=2,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_currency,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="USD, CAN",
        ),
    ],
)
event_view_checkout = Event(
    name="View Checkout",
    raised_by=actor_customer,
    received_by=actor_checkout_service,
    aggregates=[
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=aggregate_shopping_cart,
        ),
        EventAggregate(
            cardinality=Cardinality.ONE_OR_MORE,
            aggregate=view_checkout_shopping_cart_line,
        ),
    ],
    description="User views checkout page",
    kpi="# of items removed from cart/WAB",
)

semantictype_coupon_code = SemanticType(
    name="Coupon Code",
    classification=DataClassification.INTERNAL,
    variety=Variety.LIMITED_SUBSET,
)
semantictype_shipping_method = SemanticType(
    name="Shipping Method",
    classification=DataClassification.INTERNAL,
    variety=Variety.LIMITED_SUBSET,
)
semantictype_country_code = SemanticType(
    name="Country Code",
    classification=DataClassification.INTERNAL,
    variety=Variety.LIMITED_SUBSET,
)
semantictype_country_administrative_division = SemanticType(
    name="Country Administrative Division",
    classification=DataClassification.INTERNAL,
    variety=Variety.LIMITED_SUBSET,
)
semantictype_city = SemanticType(
    name="City",
    classification=DataClassification.PRIVATE,
    variety=Variety.LIMITED_SUBSET,
)
propertyattribute_payment_method = PropertyAttribute(
    name="Payment Method",
    semantic_type=semantictype_payment_method,
)
propertyattribute_gift_card_used = PropertyAttribute(
    name="Gift Card Used",
    semantic_type=semantictype_boolean,
)
propertyattribute_shipping_total = PropertyAttribute(
    name="Shipping Total",
    semantic_type=semantictype_money,
)
propertyattribute_tax_total = PropertyAttribute(
    name="Tax Total",
    semantic_type=semantictype_money,
)
propertyattribute_coupon_code = PropertyAttribute(
    name="Coupon Code",
    semantic_type=semantictype_coupon_code,
)
propertyattribute_shipping_method = PropertyAttribute(
    name="Shipping Method",
    semantic_type=semantictype_shipping_method,
)
propertyattribute_shipping_country = PropertyAttribute(
    name="Shipping Country",
    semantic_type=semantictype_country_code,
)
propertyattribute_shipping_state = PropertyAttribute(
    name="Shipping State",
    semantic_type=semantictype_country_administrative_division,
)
propertyattribute_shipping_city = PropertyAttribute(
    name="Shipping City",
    semantic_type=semantictype_city,
)
propertyattribute_of_items = PropertyAttribute(
    name="# of Items",
    semantic_type=semantictype_whole_number,
)
propertyattribute_signed_up_for_emails = PropertyAttribute(
    name="Signed Up For Emails",
    semantic_type=semantictype_boolean,
)
aggregate_payment = Aggregate(
    name="Payment",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_payment_method,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="Credit",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_gift_card_used,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=True,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_shipping_total,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=3.99,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_tax_total,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=2.5,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_subtotal,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=16.99,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_order_total,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=19.99,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_coupon_code,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="SPRING",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_currency,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="USD, CAN",
        ),
    ],
)
aggregate_shipping = Aggregate(
    name="Shipping",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_shipping_method,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="2-day, Standard",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_shipping_country,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="USA",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_shipping_state,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="CA",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_shipping_city,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="San Francisco",
        ),
    ],
)
purchase_completed_shopping_cart = Aggregate(
    name="Shopping Cart",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_of_items,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=3,
        )
    ],
)
purchase_completed_user_profile = Aggregate(
    name="User Profile",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_signed_up_for_emails,
            source=None,
            timing=None,
            type="User Property",
            sample_values=True,
        )
    ],
)
event_purchase_completed = Event(
    name="Purchase Completed",
    raised_by=actor_customer,
    received_by=actor_checkout_service,
    aggregates=[
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=aggregate_payment,
        ),
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=aggregate_shipping,
        ),
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=purchase_completed_shopping_cart,
        ),
        EventAggregate(
            cardinality=Cardinality.ONLY_ONE,
            aggregate=purchase_completed_user_profile,
        ),
    ],
    description="User completes purchase",
    kpi="# of Purchases / Weekly Active Buyers (WAB),Average purchase price,Time to convert,Bought Items/Searches,Active Buyers (6-month window)\n,First Purchase Completed within 7 Days of Account Creation,7-Day Retention",
)

actor_order_history_service = Actor(name="Order History Service")
purchased_item_shopping_cart_line = Aggregate(
    name="Shopping Cart Line",
    properties=[
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_item_id,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=123456,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_item_type,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="Classic",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_item_name,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="Socks",
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_price,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=5.99,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_quantity,
            source=None,
            timing=None,
            type="Event Property",
            sample_values=2,
        ),
        Property(
            cardinality=Cardinality.ONLY_ONE,
            attribute=propertyattribute_currency,
            source=None,
            timing=None,
            type="Event Property",
            sample_values="USD, CAN",
        ),
    ],
)
event_purchased_item = Event(
    name="Purchased Item",
    raised_by=actor_customer,
    received_by=actor_order_history_service,
    aggregates=[
        EventAggregate(
            cardinality=Cardinality.ONE_OR_MORE,
            aggregate=purchased_item_shopping_cart_line,
        )
    ],
    description="Item details purchased by the user",
    kpi="Bought Items/Searches",
)
