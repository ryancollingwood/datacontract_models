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

  def to_contract(self):
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

  def to_contract(self):
    allows_zero = self.cardinality in [Cardinality.ZERO_OR_ONE, Cardinality.ZERO_OR_MANY]

    result = {
      'semantic_type': self.attribute.semantic_type.get_meta_schema_label(),
      'is_identifier': self.is_identifier,
      'optional': allows_zero,
    }

    if self.source:
      result['source'] = self.source.to_contract()

    if self.cardinality not in [Cardinality.ONLY_ONE, Cardinality.ZERO_OR_ONE]:
      result['type'] = 'list'
    
    return result

class Aggregate(MetaSchemaModel):
  properties: List[Property]
  
  def to_contract(self):
    return {
      self.name: [{p.get_meta_schema_label():p.to_contract() for p in self.properties}]
    }

class EventAggregate(MetaSchemaContainerModel):
  aggregate: Aggregate

  def name(self):
    return self.aggregate.name

  def to_contract(self):
    allows_zero = self.cardinality in [Cardinality.ZERO_OR_ONE, Cardinality.ZERO_OR_MANY]
    result = self.aggregate.to_contract()
    result['optional'] = allows_zero
    if self.cardinality not in [Cardinality.ONLY_ONE, Cardinality.ZERO_OR_ONE]:
      result['type'] = 'list'
    return result

class Actor(MetaSchemaModel):
  pass

class Event(MetaSchemaModel):
  raised_by: Actor
  received_by: Actor
  aggregates: List[EventAggregate]

  def to_contract(self):
    result = {
      'event_name': self.name,
      'raised_by': self.raised_by.name,
      'received_by': self.received_by.name,
      'data': [a.to_contract() for a in self.aggregates]
    }
    return result
