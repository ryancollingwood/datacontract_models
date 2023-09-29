from typing import Any, Optional, Dict

from pydantic import Field, model_validator

from models import Cardinality, SchemaType, DataClassification

from .capture_sheet_base_model import CaptureSheetBaseModel


class CaptureSheetRowModel(CaptureSheetBaseModel):
    event: str
    raised_by: str
    received_by: str
    entity: str
    entity_cardinality: Cardinality
    attribute: str
    attribute_cardinality: Cardinality
    semantic_type: str
    data_classification: DataClassification = Field(default=DataClassification.UNSPECIFIED)
    schema_type: SchemaType
    column: Optional[str | None] = Field(default = None)
    table: Optional[str | None] = Field(default = None)
    database: Optional[str | None] = Field(default = None)
    not_null: Optional[bool | None] = Field(default = None)
    is_unique: Optional[bool | None] = Field(default = None)
    reference_table: Optional[str | None] = Field(default = None)
    reference_column: Optional[str | None] = Field(default = None)
    reference_database: Optional[str | None] = Field(default = None)

    @classmethod
    def is_specified(cls, value: Any):
        result = value is not None
        if isinstance(value, str):
            if value.strip() == "":
                return False
        return result

    @model_validator(mode="after")
    def check_source(cls, value: "CaptureSheetRowModel"):
        column_specified = cls.is_specified(value.column)
        table_specified = cls.is_specified(value.table)
        database_specified = cls.is_specified(value.database)
        not_null_specified = cls.is_specified(value.not_null)
        is_unique_specified = cls.is_specified(value.is_unique)

        if column_specified or table_specified or database_specified:
            msg = "If any of database, table, column is specified - all must be specified"
            assert all([column_specified, table_specified, database_specified]), msg

        if column_specified and table_specified and database_specified:
            msg = (
                "If table and column are specified"
                " - not_null and is_unique must be specified"
            )
            assert all([not_null_specified, is_unique_specified]), msg

        return value

    @model_validator(mode="after")
    def check_reference(cls, value: "CaptureSheetRowModel"):
        ref_database_specified = cls.is_specified(value.reference_database)
        ref_table_specified = cls.is_specified(value.reference_table)
        ref_column_specified = cls.is_specified(value.reference_column)

        if ref_column_specified or ref_table_specified or ref_database_specified:
            msg = (
                "If any of ref_database_specified, ref_table_specified, reference_column is specified"
                " - all must be specified"
            )
            assert all([ref_column_specified, ref_table_specified, ref_database_specified]), msg

        return value
