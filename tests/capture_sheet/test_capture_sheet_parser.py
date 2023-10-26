from capture_sheet.models.capture_sheet_model import CaptureSheetModel
from capture_sheet.models.capture_sheet_row_model import CaptureSheetRowModel
from capture_sheet.column_remapper import ColumnRemapper
from capture_sheet.parse import CaptureSheetParser
from models import Cardinality, DataClassification, SchemaType, Variety


def __rows():
    return [
        CaptureSheetRowModel(
            event="Sign Up Completed",
            raised_by="Customer",
            received_by="Identity Service",
            entity="User Registration",
            entity_cardinality=Cardinality.ONLY_ONE,
            attribute="User ID",
            attribute_cardinality=Cardinality.ONLY_ONE,
            attribute_timing=None,
            semantic_type="User ID",
            data_classification=DataClassification.INTERNAL,
            data_variety=Variety.GLOBALLY_UNIQUE,
            schema_type=SchemaType.STR,
            column="user_id",
            table="registrations",
            database="ecommerce",
            not_null=True,
            is_unique=True,
            reference_table="users",
            reference_column="id",
            reference_database="ecommerce",
            description="User successfully signs up",
            kpi="First Purchase Completed within 7 Days of Account Creation",
            type="User Property",
            sample_values="c81159b1-2658-5fba-b59b-16a0d4e30217",
            alias="Unique User ID",
            dbo="ecommerce.registrations.user_id",
        ),
        CaptureSheetRowModel(
            event="Sign Up Completed",
            raised_by="Customer",
            received_by="Identity Service",
            entity="User Registration",
            entity_cardinality=Cardinality.ONLY_ONE,
            attribute="Registration Date",
            attribute_cardinality=Cardinality.ONLY_ONE,
            attribute_timing=None,
            semantic_type="Date",
            data_classification=DataClassification.INTERNAL,
            data_variety=Variety.VARIABLE,
            schema_type=SchemaType.DATE,
            column="registered_at",
            table="registrations",
            database="ecommerce",
            not_null=True,
            is_unique=False,
            reference_table=None,
            reference_column=None,
            reference_database=None,
            description="User successfully signs up",
            kpi="First Purchase Completed within 7 Days of Account Creation",
            type="User Property",
            sample_values="YYYY-MM-DDTHH:MM:SS",
            dbo="ecommerce.registrations.registered_at",
        ),
        CaptureSheetRowModel(
            event="Sign Up Completed",
            raised_by="Customer",
            received_by="Identity Service",
            entity="User Registration",
            entity_cardinality=Cardinality.ONLY_ONE,
            attribute="Registration Method",
            attribute_cardinality=Cardinality.ONLY_ONE,
            attribute_timing=None,
            semantic_type="Identity Provider",
            data_classification=DataClassification.INTERNAL,
            data_variety=Variety.LIMITED_SUBSET,
            schema_type=SchemaType.STR,
            column="registration_provider_id",
            table="registrations",
            database="ecommerce",
            not_null=True,
            is_unique=False,
            reference_table="login_providers",
            reference_column="id",
            reference_database="ecommerce",
            description="User successfully signs up",
            kpi="First Purchase Completed within 7 Days of Account Creation",
            type="User Property",
            sample_values="Google, Facebook, E-mail",
            dbo="ecommerce.registrations.registration_provider_id",
        ),
        CaptureSheetRowModel(
            event="Sign Up Completed",
            raised_by="Customer",
            received_by="Identity Service",
            entity="User Profile",
            entity_cardinality=Cardinality.ONLY_ONE,
            attribute="Enabled Permissions",
            attribute_cardinality=Cardinality.ZERO_OR_MANY,
            attribute_timing=None,
            semantic_type="Permission",
            data_classification=DataClassification.CONFIDENTIAL,
            data_variety=Variety.LIMITED_SUBSET,
            schema_type=SchemaType.STR,
            column="granted_permissions",
            table="registrations",
            database="ecommerce",
            not_null=False,
            is_unique=False,
            reference_table="permissions",
            reference_column="id",
            reference_database="ecommerce",
            description="User successfully signs up",
            kpi="First Purchase Completed within 7 Days of Account Creation",
            type="User Property",
            sample_values='["Touch ID", "Face ID"]',
            dbo="ecommerce.registrations.granted_permissions",
        ),
        CaptureSheetRowModel(
            event="Sign Up Completed",
            raised_by="Customer",
            received_by="Identity Service",
            entity="User Profile",
            entity_cardinality=Cardinality.ONLY_ONE,
            attribute="Referred",
            attribute_cardinality=Cardinality.ONLY_ONE,
            attribute_timing=None,
            semantic_type="Referral Status",
            data_classification=DataClassification.INTERNAL,
            data_variety=Variety.LIMITED_SUBSET,
            schema_type=SchemaType.BOOLEAN,
            column="is_referral",
            table="registrations",
            database="ecommerce",
            not_null=True,
            is_unique=False,
            reference_table=None,
            reference_column=None,
            reference_database=None,
            description="User successfully signs up",
            kpi="First Purchase Completed within 7 Days of Account Creation",
            type="User Property",
            sample_values=True,
            dbo="ecommerce.registrations.is_referral",
        ),
        CaptureSheetRowModel(
            event="Sign Up Completed",
            raised_by="Customer",
            received_by="Identity Service",
            entity="User Profile",
            entity_cardinality=Cardinality.ONLY_ONE,
            attribute="Payment Methods Added",
            attribute_cardinality=Cardinality.ZERO_OR_MANY,
            attribute_timing=None,
            semantic_type="Payment Method",
            data_classification=DataClassification.RESTRICTED,
            data_variety=Variety.LIMITED_SUBSET,
            schema_type=SchemaType.STR,
            column="payment_methods",
            table="registrations",
            database="ecommerce",
            not_null=False,
            is_unique=False,
            reference_table="payment_methods",
            reference_column="id",
            reference_database="ecommerce",
            description="User successfully signs up",
            kpi="First Purchase Completed within 7 Days of Account Creation",
            type="User Property",
            sample_values='["Credit", "Debit"]',
            dbo="ecommerce.registrations.payment_methods",
        ),
        CaptureSheetRowModel(
            event="Sign Up Completed",
            raised_by="Customer",
            received_by="Identity Service",
            entity="User Profile",
            entity_cardinality=Cardinality.ONLY_ONE,
            attribute="Login Method",
            attribute_cardinality=Cardinality.ONLY_ONE,
            attribute_timing=None,
            semantic_type="Identity Provider",
            data_classification=DataClassification.INTERNAL,
            data_variety=Variety.LIMITED_SUBSET,
            schema_type=SchemaType.STR,
            column="login_provider_id",
            table="registrations",
            database="ecommerce",
            not_null=True,
            is_unique=False,
            reference_table="login_providers",
            reference_column="id",
            reference_database="ecommerce",
            description="User successfully signs up",
            kpi="First Purchase Completed within 7 Days of Account Creation",
            type="Event Property",
            sample_values="Email, Facebook, Google",
            dbo="ecommerce.registrations.login_provider_id",
        ),
    ]


def __column_remapper():
    return ColumnRemapper(
        original_columns=[
            "event",
            "event_description",
            "kpi",
            "raised_by",
            "received_by",
            "entity",
            "entity_cardinality",
            "property_type",
            "attribute",
            "attribute_cardinality",
            "attribute_alias",
            "semantic_type",
            "sample_values",
            "variety",
            "classification",
            "schema_type",
            "column",
            "table",
            "database",
            "not_null",
            "is_unique",
            "reference_column",
            "reference_table",
            "reference_database",
            "attribute_timing",
        ],
        renamed_columns={
            "event": "event",
            "event_description": "description",
            "kpi": "kpi",
            "raised_by": "raised_by",
            "received_by": "received_by",
            "entity": "entity",
            "entity_cardinality": "entity_cardinality",
            "attribute": "attribute",
            "property_type": "type",
            "sample_values": "sample_values",
            "attribute_cardinality": "attribute_cardinality",
            "attribute_timing": "attribute_timing",
            "semantic_type": "semantic_type",
            "attribute_alias": "alias",
            "classification": "classification",
            "variety": "variety",
            "schema_type": "schema_type",
            "database": "database",
            "table": "table",
            "column": "column",
            "not_null": "not_null",
            "is_unique": "is_unique",
            "reference_database": "reference_database",
            "reference_table": "reference_table",
            "reference_column": "reference_column",
        },
        sorted_columns=[
            "event",
            "description",
            "kpi",
            "raised_by",
            "received_by",
            "entity",
            "entity_cardinality",
            "attribute",
            "type",
            "sample_values",
            "attribute_cardinality",
            "attribute_timing",
            "semantic_type",
            "alias",
            "classification",
            "variety",
            "schema_type",
            "database",
            "table",
            "column",
            "not_null",
            "is_unique",
            "reference_database",
            "reference_table",
            "reference_column",
        ],
        custom_columns=[
            "event_description",
            "kpi",
            "property_type",
            "sample_values",
            "attribute_alias",
        ],
        column_map={
            "event_": ["event", "description", "kpi", "raised_by", "received_by"],
            "entity_": ["entity", "entity_cardinality"],
            "property_": [
                "attribute",
                "type",
                "sample_values",
                "attribute_cardinality",
                "attribute_timing",
            ],
            "attribute_": ["semantic_type", "alias", "classification", "variety"],
            "source_": [
                "schema_type",
                "database",
                "table",
                "column",
                "not_null",
                "is_unique",
            ],
            "reference_": ["reference_database", "reference_table", "reference_column"],
        },
        known_keys=[
            "event_",
            "entity_",
            "property_",
            "attribute_",
            "source_",
            "reference_",
        ],
        known_columns=[
            "event",
            "raised_by",
            "received_by",
            "entity",
            "entity_cardinality",
            "attribute",
            "attribute_cardinality",
            "attribute_timing",
            "semantic_type",
            "classification",
            "variety",
            "schema_type",
            "database",
            "table",
            "column",
            "not_null",
            "is_unique",
            "reference_database",
            "reference_table",
            "reference_column",
        ],
    )


def test_create_capture_sheet_parser():
    rows = __rows()
    column_remapper = __column_remapper()

    CaptureSheetParser(rows, column_remapper)


def test_parse_capture_sheet_parser():
    from models import (
        Cardinality,
        DataClassification,
        SchemaType,
        Variety,
        Event,
        Actor,
        Aggregate,
        Database,
        DatabaseColumn,
        DatabasePath,
        DatabaseTable,
        EventAggregate,
        Property,
        PropertyAttribute,
        SemanticType,
        MetaTiming,
    )

    rows = __rows()
    column_remapper = __column_remapper()

    expected_actors = {
        "Customer": Actor(name="Customer"),
        "Identity Service": Actor(name="Identity Service"),
    }

    expected_databases = {"ecommerce": Database(name="ecommerce")}

    expected_database_tables = {
        "registrations": DatabaseTable(
            name="registrations", database=expected_databases["ecommerce"]
        )
    }

    expected_database_references = {
        "ecommerce.users.id": DatabasePath(
            database="ecommerce", table="users", column="id"
        ),
        "ecommerce.login_providers.id": DatabasePath(
            database="ecommerce", table="login_providers", column="id"
        ),
        "ecommerce.permissions.id": DatabasePath(
            database="ecommerce", table="permissions", column="id"
        ),
        "ecommerce.payment_methods.id": DatabasePath(
            database="ecommerce", table="payment_methods", column="id"
        ),
    }

    expected_semantic_types = {
        "User ID": SemanticType(
            name="User ID",
            classification=DataClassification.INTERNAL,
            variety=Variety.GLOBALLY_UNIQUE,
        ),
        "Date": SemanticType(
            name="Date",
            classification=DataClassification.INTERNAL,
            variety=Variety.VARIABLE,
        ),
        "Identity Provider": SemanticType(
            name="Identity Provider",
            classification=DataClassification.INTERNAL,
            variety=Variety.LIMITED_SUBSET,
        ),
        "Permission": SemanticType(
            name="Permission",
            classification=DataClassification.CONFIDENTIAL,
            variety=Variety.LIMITED_SUBSET,
        ),
        "Referral Status": SemanticType(
            name="Referral Status",
            classification=DataClassification.INTERNAL,
            variety=Variety.LIMITED_SUBSET,
        ),
        "Payment Method": SemanticType(
            name="Payment Method",
            classification=DataClassification.RESTRICTED,
            variety=Variety.LIMITED_SUBSET,
        ),
    }

    expected_property_attributes = {
        "User ID": PropertyAttribute(
            name="User ID",
            semantic_type=expected_semantic_types["User ID"],
            alias="Unique User ID",
        ),
        "Registration Date": PropertyAttribute(
            name="Registration Date",
            semantic_type=expected_semantic_types["Date"],
        ),
        "Registration Method": PropertyAttribute(
            name="Registration Method",
            semantic_type=expected_semantic_types["Identity Provider"],
        ),
        "Enabled Permissions": PropertyAttribute(
            name="Enabled Permissions",
            semantic_type=expected_semantic_types["Permission"],
        ),
        "Referred": PropertyAttribute(
            name="Referred", semantic_type=expected_semantic_types["Referral Status"]
        ),
        "Payment Methods Added": PropertyAttribute(
            name="Payment Methods Added",
            semantic_type=expected_semantic_types["Payment Method"],
        ),
        "Login Method": PropertyAttribute(
            name="Login Method",
            semantic_type=expected_semantic_types["Identity Provider"],
        ),
    }

    expected_database_columns = {
        "user_id": DatabaseColumn(
            name="user_id",
            table=expected_database_tables["registrations"],
            schema_type=SchemaType.STR,
            not_null=True,
            is_unique=True,
            references=DatabasePath(database="ecommerce", table="users", column="id"),
        ),
        "registered_at": DatabaseColumn(
            name="registered_at",
            table=expected_database_tables["registrations"],
            schema_type=SchemaType.DATE,
            not_null=True,
            is_unique=False,
            references=None,
        ),
        "registration_provider_id": DatabaseColumn(
            name="registration_provider_id",
            table=expected_database_tables["registrations"],
            schema_type=SchemaType.STR,
            not_null=True,
            is_unique=False,
            references=expected_database_references["ecommerce.login_providers.id"],
        ),
        "granted_permissions": DatabaseColumn(
            name="granted_permissions",
            table=expected_database_tables["registrations"],
            schema_type=SchemaType.STR,
            not_null=False,
            is_unique=False,
            references=expected_database_references["ecommerce.permissions.id"],
        ),
        "is_referral": DatabaseColumn(
            name="is_referral",
            table=expected_database_tables["registrations"],
            schema_type=SchemaType.BOOLEAN,
            not_null=True,
            is_unique=False,
            references=None,
        ),
        "payment_methods": DatabaseColumn(
            name="payment_methods",
            table=expected_database_tables["registrations"],
            schema_type=SchemaType.STR,
            not_null=False,
            is_unique=False,
            references=expected_database_references["ecommerce.payment_methods.id"],
        ),
        "login_provider_id": DatabaseColumn(
            name="login_provider_id",
            table=expected_database_tables["registrations"],
            schema_type=SchemaType.STR,
            not_null=True,
            is_unique=False,
            references=expected_database_references["ecommerce.login_providers.id"],
        ),
    }

    expected_aggregates = {
        "User Registration": Aggregate(
            name="User Registration",
            properties=[
                Property(
                    cardinality=Cardinality.ONLY_ONE,
                    attribute=expected_property_attributes["User ID"],
                    source=expected_database_columns["user_id"],
                    timing=None,
                    type="User Property",
                    sample_values="c81159b1-2658-5fba-b59b-16a0d4e30217",
                ),
                Property(
                    cardinality=Cardinality.ONLY_ONE,
                    attribute=expected_property_attributes["Registration Date"],
                    source=expected_database_columns["registered_at"],
                    timing=MetaTiming.UNSPECIFIED,
                    type="User Property",
                    sample_values="YYYY-MM-DDTHH:MM:SS",
                ),
                Property(
                    cardinality=Cardinality.ONLY_ONE,
                    attribute=expected_property_attributes["Registration Method"],
                    source=expected_database_columns["registration_provider_id"],
                    timing=None,
                    type="User Property",
                    sample_values="Google, Facebook, E-mail",
                ),
            ],
        ),
        "User Profile": Aggregate(
            name="User Profile",
            properties=[
                Property(
                    cardinality=Cardinality.ZERO_OR_MANY,
                    attribute=expected_property_attributes["Enabled Permissions"],
                    source=expected_database_columns["granted_permissions"],
                    timing=None,
                    type="User Property",
                    sample_values='["Touch ID", "Face ID"]',
                ),
                Property(
                    cardinality=Cardinality.ONLY_ONE,
                    attribute=expected_property_attributes["Referred"],
                    source=expected_database_columns["is_referral"],
                    timing=None,
                    type="User Property",
                    sample_values=True,
                ),
                Property(
                    cardinality=Cardinality.ZERO_OR_MANY,
                    attribute=expected_property_attributes["Payment Methods Added"],
                    source=expected_database_columns["payment_methods"],
                    timing=None,
                    type="User Property",
                    sample_values='["Credit", "Debit"]',
                ),
                Property(
                    cardinality=Cardinality.ONLY_ONE,
                    attribute=expected_property_attributes["Login Method"],
                    source=expected_database_columns["login_provider_id"],
                    timing=None,
                    type="Event Property",
                    sample_values="Email, Facebook, Google",
                ),
            ],
        ),
    }

    expected_events = {
        "Sign Up Completed": Event(
            name="Sign Up Completed",
            raised_by=expected_actors["Customer"],
            received_by=expected_actors["Identity Service"],
            aggregates=[
                EventAggregate(
                    cardinality=Cardinality.ONLY_ONE,
                    aggregate=expected_aggregates["User Registration"],
                ),
                EventAggregate(
                    cardinality=Cardinality.ONLY_ONE,
                    aggregate=expected_aggregates["User Profile"],
                ),
            ],
            description="User successfully signs up",
            kpi="First Purchase Completed within 7 Days of Account Creation",
        )
    }

    result: CaptureSheetModel = CaptureSheetParser(rows, column_remapper).parse()

    assert result.actors == expected_actors, "Actors did not match."

    assert result.databases == expected_databases, "Databases did not match."
    assert result.database_tables == expected_database_tables, "Database tables did not match."
    assert result.database_columns == expected_database_columns, "Database columns did not match."
    assert result.database_references == expected_database_references, "Database references did not match."

    assert result.semantic_types == expected_semantic_types, "Semantic types did not match."
    assert result.property_attributes == expected_property_attributes, "Property attributes did not match."
    assert result.aggregates == expected_aggregates, "Aggregates did not match."

    assert result.events == expected_events, "Events did not match."
