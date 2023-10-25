from pydantic import ValidationError
from capture_sheet.models.capture_sheet_row_model import CaptureSheetRowModel
from models import Cardinality, DataClassification, Variety, SchemaType


def test_create_row():
    row = CaptureSheetRowModel(
        event="Sign Up Completed",
        raised_by="Customer",
        received_by="Identity Service",
        entity="User Registration",
        entity_cardinality="OnlyOne",
        attribute="User ID",
        attribute_cardinality="OnlyOne",
        semantic_type="User ID",
        data_classification="Internal",
        data_variety="GloballyUnique",
        schema_type="str",
        column="user_id",
        table="registrations",
        database="ecommerce",
        not_null=True,
        is_unique=True,
        reference_table="users",
        reference_column="id",
        reference_database="ecommerce",
    )

    assert row.event == "Sign Up Completed"
    assert row.entity_cardinality == Cardinality.ONLY_ONE
    assert row.attribute_cardinality == Cardinality.ONLY_ONE
    assert row.data_classification == DataClassification.INTERNAL
    assert row.data_variety == Variety.GLOBALLY_UNIQUE
    assert row.schema_type == SchemaType.STR


def test_column_not_specified():
    try:
        row = CaptureSheetRowModel(
            event="Sign Up Completed",
            raised_by="Customer",
            received_by="Identity Service",
            entity="User Registration",
            entity_cardinality="OnlyOne",
            attribute="User ID",
            attribute_cardinality="OnlyOne",
            semantic_type="User ID",
            data_classification="Internal",
            data_variety="GloballyUnique",
            schema_type="str",
            # column = "user_id",
            table="registrations",
            database="ecommerce",
            not_null=True,
            is_unique=True,
            reference_table="users",
            reference_column="id",
            reference_database="ecommerce",
        )
    except ValidationError as e:
        assert (
            str(e).find(
                "If any of database, table, column is specified - all must be specified"
            )
            > -1
        )


def test_table_not_specified():
    try:
        row = CaptureSheetRowModel(
            event="Sign Up Completed",
            raised_by="Customer",
            received_by="Identity Service",
            entity="User Registration",
            entity_cardinality="OnlyOne",
            attribute="User ID",
            attribute_cardinality="OnlyOne",
            semantic_type="User ID",
            data_classification="Internal",
            data_variety="GloballyUnique",
            schema_type="str",
            column="user_id",
            # table="registrations",
            database="ecommerce",
            not_null=True,
            is_unique=True,
            reference_table="users",
            reference_column="id",
            reference_database="ecommerce",
        )
    except ValidationError as e:
        assert (
            str(e).find(
                "If any of database, table, column is specified"
                " - all must be specified"
            )
            > -1
        )


def test_database_not_specified():
    try:
        row = CaptureSheetRowModel(
            event="Sign Up Completed",
            raised_by="Customer",
            received_by="Identity Service",
            entity="User Registration",
            entity_cardinality="OnlyOne",
            attribute="User ID",
            attribute_cardinality="OnlyOne",
            semantic_type="User ID",
            data_classification="Internal",
            data_variety="GloballyUnique",
            schema_type="str",
            column="user_id",
            table="registrations",
            # database="ecommerce",
            not_null=True,
            is_unique=True,
            reference_table="users",
            reference_column="id",
            reference_database="ecommerce",
        )
    except ValidationError as e:
        assert (
            str(e).find(
                "If any of database, table, column is specified"
                " - all must be specified"
            )
            > -1
        )


def test_schema_not_specified():
    try:
        row = CaptureSheetRowModel(
            event="Sign Up Completed",
            raised_by="Customer",
            received_by="Identity Service",
            entity="User Registration",
            entity_cardinality="OnlyOne",
            attribute="User ID",
            attribute_cardinality="OnlyOne",
            semantic_type="User ID",
            data_classification="Internal",
            data_variety="GloballyUnique",
            schema_type="str",
            column="user_id",
            table="registrations",
            database="ecommerce",
            # not_null=True,
            # is_unique=True,
            reference_table="users",
            reference_column="id",
            reference_database="ecommerce",
        )
    except ValidationError as e:
        assert (
            str(e).find(
                "If table and column are specified"
                " - not_null and is_unique must be specified"
            )
            > -1
        )



def test_ref_column_not_specified():
    try:
        row = CaptureSheetRowModel(
            event="Sign Up Completed",
            raised_by="Customer",
            received_by="Identity Service",
            entity="User Registration",
            entity_cardinality="OnlyOne",
            attribute="User ID",
            attribute_cardinality="OnlyOne",
            semantic_type="User ID",
            data_classification="Internal",
            data_variety="GloballyUnique",
            schema_type="str",
            column = "user_id",
            table="registrations",
            database="ecommerce",
            not_null=True,
            is_unique=True,
            reference_table="users",
            # reference_column="id",
            reference_database="ecommerce",
        )
    except ValidationError as e:
        assert (
            str(e).find(
                "If any of ref_database_specified, ref_table_specified, reference_column is specified"
                " - all must be specified"            
                )
            > -1
        )


def test_ref_table_not_specified():
    try:
        row = CaptureSheetRowModel(
            event="Sign Up Completed",
            raised_by="Customer",
            received_by="Identity Service",
            entity="User Registration",
            entity_cardinality="OnlyOne",
            attribute="User ID",
            attribute_cardinality="OnlyOne",
            semantic_type="User ID",
            data_classification="Internal",
            data_variety="GloballyUnique",
            schema_type="str",
            column="user_id",
            table="registrations",
            database="ecommerce",
            not_null=True,
            is_unique=True,
            # reference_table="users",
            reference_column="id",
            reference_database="ecommerce",
        )
    except ValidationError as e:
        assert (
            str(e).find(
                "If any of ref_database_specified, ref_table_specified, reference_column is specified"
                " - all must be specified"
            )
            > -1
        )


def test_ref_database_not_specified():
    try:
        row = CaptureSheetRowModel(
            event="Sign Up Completed",
            raised_by="Customer",
            received_by="Identity Service",
            entity="User Registration",
            entity_cardinality="OnlyOne",
            attribute="User ID",
            attribute_cardinality="OnlyOne",
            semantic_type="User ID",
            data_classification="Internal",
            data_variety="GloballyUnique",
            schema_type="str",
            column="user_id",
            table="registrations",
            database="ecommerce",
            not_null=True,
            is_unique=True,
            reference_table="users",
            reference_column="id",
            # reference_database="ecommerce",
        )
    except ValidationError as e:
        assert (
            str(e).find(
                "If any of ref_database_specified, ref_table_specified, reference_column is specified"
                " - all must be specified"
            )
            > -1
        )

def test_variety_schematype_not_specified():
    try:
        row = CaptureSheetRowModel(
            event="Sign Up Completed",
            raised_by="Customer",
            received_by="Identity Service",
            entity="User Registration",
            entity_cardinality="OnlyOne",
            attribute="User ID",
            attribute_cardinality="OnlyOne",
            semantic_type="User ID",
            data_classification="Internal",
            data_variety="GloballyUnique",
            schema_type="UNSPECIFIED",
            column="user_id",
            table="registrations",
            database="ecommerce",
            not_null=True,
            is_unique=True,
            reference_table="users",
            reference_column="id",
            reference_database="ecommerce",
        )
    except ValidationError as e:
        assert (
            str(e).find(
                "If data_variety is specified - schema_type must be specified"
            )
            > -1
        )

def test_variety_unique_not_specified():
    try:
        row = CaptureSheetRowModel(
            event="Sign Up Completed",
            raised_by="Customer",
            received_by="Identity Service",
            entity="User Registration",
            entity_cardinality="OnlyOne",
            attribute="User ID",
            attribute_cardinality="OnlyOne",
            semantic_type="User ID",
            data_classification="Internal",
            # data_variety="GloballyUnique",
            schema_type="guid",
            column="user_id",
            table="registrations",
            database="ecommerce",
            not_null=True,
            is_unique=False,
            reference_table="users",
            reference_column="id",
            reference_database="ecommerce",
        )
    except ValidationError as e:
        assert (
            str(e).find(
                "If schema_type is UUID or GUID - data_variety must be LOCALLY_UNIQUE or GLOBALLY_UNIQUE"
            )
            > -1
        )

