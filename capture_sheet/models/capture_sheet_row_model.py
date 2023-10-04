from typing import Any, Optional, Dict

from pydantic import Field, model_validator

from models import Cardinality, SchemaType, DataClassification, Variety

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
    data_classification: DataClassification = Field(default=DataClassification.UNSPECIFIED, validation_alias="classification")
    data_variety: Variety = Field(default=Variety.UNSPECIFIED, validation_alias="variety")
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
    
    @model_validator(mode="after")
    def check_schema_type_and_variety(cls, value: "CaptureSheetRowModel"):
        schema_type_specified = value.schema_type.is_specified()
        variety_specified = value.data_variety.is_specified()

        if variety_specified and not schema_type_specified:
            msg = "If data_variety is specified - schema_type must be specified"
            assert schema_type_specified, msg
        
        if schema_type_specified and variety_specified:
            is_variety_unique = value.data_variety.is_unique()
            is_data_type_uid = value.schema_type.is_uid()
            if is_data_type_uid and not is_variety_unique:
                """
                GUID and UUID by definition should be GLOBALLY_UNIQUE, however allowing for the possibility
                that it's LOCALLY_UNIQUE - perhaps a future enhancement would be to raise a warning if 
                LOCALLY_UNIQUE
                """
                msg = "If schema_type is UUID or GUID - data_variety must be LOCALLY_UNIQUE or GLOBALLY_UNIQUE"
                assert not is_variety_unique, msg