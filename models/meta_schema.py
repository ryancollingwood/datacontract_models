from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Extra, Field

from models import Cardinality, SchemaType


class MetaSchemaBaseModel(BaseModel):
    model_config: ConfigDict = ConfigDict(
        str_to_lower=True, validate_default=True, extra=Extra.ignore
      )

    name: str

class SemanticType(MetaSchemaBaseModel):
  pass

class PropertyAttribute(MetaSchemaBaseModel):
  semantic_type: SemanticType

class Database(MetaSchemaBaseModel):
  pass

class DatabaseTable(MetaSchemaBaseModel):
  database: Database

class DatabaseColumn(MetaSchemaBaseModel):
  table: DatabaseTable
  schema_type: SchemaType
  not_null: bool
  is_unique: bool
  references: Optional['DatabaseColumn'] = Field(default = None)

class Property(MetaSchemaBaseModel):
  attribute: PropertyAttribute
  source: Optional[DatabaseColumn ] = Field(default = None)
  cardinality: Cardinality
  is_identifier: bool = Field(default=False)

class Aggregate(MetaSchemaBaseModel):
  properties: List[Property]

class EventAggregate(MetaSchemaBaseModel):
  aggregate: Aggregate
  cardinality: Cardinality

class Actor(MetaSchemaBaseModel):
  pass

class Event(MetaSchemaBaseModel):
  raised_by: Actor
  received_by: Actor
  aggregates: List[EventAggregate]
