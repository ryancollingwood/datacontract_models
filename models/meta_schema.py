from typing import List, Optional
from pydantic import Field, field_validator, model_validator

from .schema_type import SchemaType
from .data_classification import DataClassification
from .variety import Variety
from .meta_schema_base_model import (
    MetaSchemaBaseModel,
    MetaSchemaModel,
    MetaSchemaContainerModel,
)
from .meta_timing import MetaTiming


class SemanticType(MetaSchemaModel):
    classification: Optional[DataClassification] = Field(
        default=DataClassification.UNSPECIFIED
    )
    variety: Optional[Variety] = Field(default=Variety.UNSPECIFIED)


class PropertyAttribute(MetaSchemaModel):
    _to_contract_flatten_model: bool = True
    semantic_type: SemanticType


class DatabasePath(MetaSchemaBaseModel):
    database: str
    table: str
    column: str

    @classmethod
    def from_database_column(cls, database_column: "DatabaseColumn"):
        return cls(
            database=database_column.table.database.name,
            table=database_column.table.name,
            column=database_column.name,
        )

    @property
    def name(self):
        return f"{self.database}.{self.table}.{self.column}"


class Database(MetaSchemaModel):
    pass


class DatabaseTable(MetaSchemaModel):
    database: Database


class DatabaseColumn(MetaSchemaModel):
    table: DatabaseTable
    schema_type: SchemaType
    not_null: bool
    is_unique: bool
    references: Optional[DatabasePath] = Field(default=None)

    @property
    def dbo(self):
        return DatabasePath.from_database_column(self)

    def get_contract_items(self):
        return {
            "database": self.table.database.name,
            "table": self.table.name,
            "column": self.name,
            "schema_type": str(self.schema_type.value),
            "not_null": self.not_null,
            "is_unique": self.is_unique,
            "references": self.references.to_contract() if self.references else None,
        }


class Property(MetaSchemaContainerModel):
    attribute: PropertyAttribute
    source: Optional[DatabaseColumn] = Field(default=None)
    timing: Optional[MetaTiming] = Field(default=None)

    def name(self):
        return self.attribute.name
    
    @property
    def is_identifier(self):
        return self.attribute.semantic_type.variety.is_unique()
    
    @property
    def is_required(self):
        return self.cardinality.is_mandatory()

    @field_validator("timing")
    def get_timing(cls, v: MetaTiming, values, **kwargs):
        """
        Tried this with @computed_field but it didn't work
        So using a validator instead as per:
        https://github.com/pydantic/pydantic/issues/1928#issuecomment-692366291
        """
        source: DatabaseColumn = values.data.get("source")
        timing: MetaTiming = v
        schema_type: SchemaType = None
        is_temporal: bool = False
        is_timestamp: bool = False

        if not source and not timing:
            return None
        
        if source:
            schema_type = source.schema_type

        if schema_type:
            is_temporal = schema_type.is_temporal()
            is_timestamp = schema_type.is_timestamp()

        if source and not timing and is_temporal:
            # TODO: raise a debug message that timing is unspecified
            return MetaTiming.UNSPECIFIED
        
        if timing and source:
            if not is_temporal:
                raise ValueError(f"Timing specified for non-temporal source: {source.name}")
            if not is_timestamp:
                # TODO: raise a warning that the lack precision is suspect
                pass

        return timing
    
    @model_validator(mode="after")
    def check_schema_type_and_variety(cls, value: "Property"):
        specified_variety = value.attribute.semantic_type.variety
        specified_source = value.source

        if specified_variety and specified_source:
            if specified_source.schema_type.is_boolean() and specified_variety != Variety.LIMITED_SUBSET:
                value.attribute.semantic_type.variety = Variety.LIMITED_SUBSET
        
        return value


class Aggregate(MetaSchemaModel):
    properties: List[Property]


class EventAggregate(MetaSchemaContainerModel):
    aggregate: Aggregate
    # TODO: this is a hack to get the identifiers and required fields 
    # `repr=False` means it won't be considered in output for `__repr__`
    identifiers: Optional[List[str]] = Field(None, repr=False)
    required: Optional[List[str]] = Field(None, repr=False)

    def name(self):
        return self.aggregate.name
    
    @field_validator("identifiers")
    def get_indentifiers(cls, v, values, **kwargs):
        """
        Tried this with @computed_field but it didn't work
        So using a validator instead as per:
        https://github.com/pydantic/pydantic/issues/1928#issuecomment-692366291
        """
        result = [x.slug for x in values.data["aggregate"].properties if x.is_identifier]
        return result
    
    @field_validator("required")
    def get_required(cls, v, values, **kwargs):
        """
        Tried this with @computed_field but it didn't work
        So using a validator instead as per:
        https://github.com/pydantic/pydantic/issues/1928#issuecomment-692366291
        """
        result = [x.slug for x in values.data["aggregate"].properties if x.is_required]
        return result


class Actor(MetaSchemaModel):
    pass


class Event(MetaSchemaModel):
    raised_by: Actor
    received_by: Actor
    aggregates: List[EventAggregate]
