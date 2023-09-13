from typing import List, Optional, Dict, Any
from pydantic import Field, validator

from .schema_type import SchemaType
from .cardinality import Cardinality
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

  def get_contract_items(self):
    return {
      'database': self.table.database.name,
      'table': self.table.name,
      'column': self.name,
      'schema_type': str(self.schema_type.value),
      'not_null': self.not_null,
      'is_unique': self.is_unique,      
      'references': self.references.to_contract() if self.references else None
    }

class Property(MetaSchemaContainerModel):
  attribute: PropertyAttribute
  source: Optional[DatabaseColumn] = Field(default = None)
  is_identifier: bool = Field(default=False)
  
  def name(self):
      return self.attribute.name

class Aggregate(MetaSchemaModel):
  properties: List[Property]

class EventAggregate(MetaSchemaContainerModel):
  aggregate: Aggregate

  def name(self):
    return self.aggregate.name

class Actor(MetaSchemaModel):
  pass

class Event(MetaSchemaModel):
  raised_by: Actor
  received_by: Actor
  aggregates: List[EventAggregate]
