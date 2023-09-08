from typing import List, Optional
from pydantic import Field

from models import SchemaType
from .meta_schema_base_model import MetaSchemaModel, MetaSchemaContainerModel


class SemanticType(MetaSchemaModel):
  pass

class PropertyAttribute(MetaSchemaModel):
  semantic_type: SemanticType

class Database(MetaSchemaModel):
  pass

class DatabaseTable(MetaSchemaModel):
  database: Database

class DatabaseColumn(MetaSchemaModel):
  table: DatabaseTable
  schema_type: SchemaType
  not_null: bool
  is_unique: bool
  references: Optional['DatabaseColumn'] = Field(default = None)

class Property(MetaSchemaContainerModel):
  attribute: PropertyAttribute
  source: Optional[DatabaseColumn] = Field(default = None)
  is_identifier: bool = Field(default=False)

class Aggregate(MetaSchemaModel):
  properties: List[Property]

class EventAggregate(MetaSchemaContainerModel):
  aggregate: Aggregate

class Actor(MetaSchemaModel):
  pass

class Event(MetaSchemaModel):
  raised_by: Actor
  received_by: Actor
  aggregates: List[EventAggregate]
