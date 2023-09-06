from typing import Any
from pydantic import BaseModel, ConfigDict, Field, Extra, model_validator

from models import Cardinality, SchemaType


class CaptureSheetBaseModel(BaseModel):
    model_config: ConfigDict = ConfigDict(
        str_to_lower=True, validate_default=True, extra=Extra.ignore
    )


class CaptureSheetModel(CaptureSheetBaseModel):
    event: str
    raised_by: str
    received_by: str
    entity: str
    entity_cardinality: Cardinality
    attribute: str
    attribute_cardinality: Cardinality
    semantic_type: str
    schema_type: SchemaType
    column: str | None = Field(default=None)
    table: str | None = Field(default=True)
    database: str | None = Field(default=True)
    # TODO rename is null
    is_null: bool | None = Field(default=True)
    is_unique: bool | None = Field(default=True)
    reference_table: str | None = Field(default=None)
    reference_column: str | None = Field(default=None)

    @classmethod
    def is_specified(cls, value: Any):
        result = value is not None
        if isinstance(value, str):
            if value.strip() == "":
                return False
        return result

    @model_validator(mode="after")
    def check_source(cls, value: "CaptureSheetModel"):
        column_specified = cls.is_specified(value.column)
        table_specified = cls.is_specified(value.table)
        is_null_specified = cls.is_specified(value.is_null)
        is_unique_specified = cls.is_specified(value.is_unique)

        if column_specified or table_specified:
            msg = "If either table or column is specified - both must be specified"
            assert all([column_specified, table_specified]), msg

        if column_specified and table_specified:
            msg = (
                "If table and column are specified"
                " - is_null and is_unique must be specified"
            )
            assert all([is_null_specified, is_unique_specified]), msg

        return value

    @model_validator(mode="after")
    def check_reference(cls, value: "CaptureSheetModel"):
        ref_table_specified = cls.is_specified(value.reference_table)
        ref_column_specified = cls.is_specified(value.reference_column)

        if ref_column_specified or ref_table_specified:
            msg = (
                "If either ref_table_specified or reference_column is specified"
                " - both must be specified"
            )
            assert all([ref_column_specified, ref_table_specified]), msg

        return value
