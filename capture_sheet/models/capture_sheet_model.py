from typing import Dict
from models import (
    MetaSchemaBaseModel,
    SemanticType, PropertyAttribute, Actor, 
    Database, DatabaseTable, DatabaseColumn, SchemaType,
    Aggregate, Property, EventAggregate, Event
)

from .capture_sheet_base_model import CaptureSheetBaseModel
from .capture_sheet_row_model import CaptureSheetRowModel

class CaptureSheetModel(CaptureSheetBaseModel):
  semantic_types: Dict[str, SemanticType] = dict()
  property_attributes: Dict[str, PropertyAttribute] = dict()
  actors: Dict[str, Actor] = dict()
  databases: Dict[str, Database] = dict()
  database_tables: Dict[str, DatabaseTable] = dict()
  database_columns: Dict[str, DatabaseColumn] = dict()
  properties: Dict[str, Property] = dict()
  aggregates: Dict[str, Aggregate] = dict()
  event_aggregates: Dict[str, EventAggregate] = dict()
  events: Dict[str, Event] = dict()

  @staticmethod
  def is_present(value: str, store: Dict[str, MetaSchemaBaseModel]):
    if value is None:
      return True
    return value in store
