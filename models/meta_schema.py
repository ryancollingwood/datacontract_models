from typing import List, Optional
from pydantic import Field

from .schema_type import SchemaType
from .cardinality import Cardinality
from .data_classification import DataClassification
from .meta_schema_base_model import MetaSchemaBaseModel, MetaSchemaModel, MetaSchemaContainerModel


class SemanticType(MetaSchemaModel):
  classification: Optional[DataClassification] = Field(default=DataClassification.UNSPECIFIED)

class PropertyAttribute(MetaSchemaModel):
  _to_contract_flatten_model: bool = True
  semantic_type: SemanticType

class DatabasePath(MetaSchemaBaseModel):
  database: str
  table: str
  column: str

  @classmethod
  def from_database_column(cls, database_column: 'DatabaseColumn'):
    return cls(
      database=database_column.table.database.name,
      table=database_column.table.name,
      column=database_column.name
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
  references: Optional[DatabasePath] = Field(default = None)

  @property
  def dbo(self):
    return DatabasePath.from_database_column(self)

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
