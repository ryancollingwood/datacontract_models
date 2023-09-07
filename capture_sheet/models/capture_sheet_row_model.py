from typing import Any, Optional

from pydantic import Field, model_validator

from models import Cardinality, SchemaType

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
    schema_type: SchemaType
    column: Optional[str | None] = Field(default = None)
    table: Optional[str | None] = Field(default = None)
    database: Optional[str | None] = Field(default = None)
    not_null: Optional[bool | None] = Field(default = None)
    is_unique: Optional[bool | None] = Field(default = None)
    reference_table: Optional[str | None] = Field(default = None)
    reference_column: Optional[str | None] = Field(default = None)

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
        not_null_specified = cls.is_specified(value.not_null)
        is_unique_specified = cls.is_specified(value.is_unique)

        if column_specified or table_specified:
            msg = "If either table or column is specified - both must be specified"
            assert all([column_specified, table_specified]), msg

        if column_specified and table_specified:
            msg = (
                "If table and column are specified"
                " - not_null and is_unique must be specified"
            )
            assert all([not_null_specified, is_unique_specified]), msg

        return value

    @model_validator(mode="after")
    def check_reference(cls, value: "CaptureSheetRowModel"):
        ref_table_specified = cls.is_specified(value.reference_table)
        ref_column_specified = cls.is_specified(value.reference_column)

        if ref_column_specified or ref_table_specified:
            msg = (
                "If either ref_table_specified or reference_column is specified"
                " - both must be specified"
            )
            assert all([ref_column_specified, ref_table_specified]), msg

        return value
