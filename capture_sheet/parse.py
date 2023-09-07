from pathlib import Path
from typing import Dict, List
import json
from dataclasses import dataclass
from models import (
    MetaSchemaBaseModel,
    SemanticType,
    PropertyAttribute,
    Actor,
    Database,
    DatabaseTable,
    DatabaseColumn,
    Aggregate,
    Property,
    EventAggregate,
    Event,
)
from models import SchemaType, Actor, Cardinality

from .models.capture_sheet_model import CaptureSheetModel
from .models.capture_sheet_row_model import CaptureSheetRowModel
from .column_names import RESULT, OUTCOME

@dataclass
class LastEvent:
    name: str
    raised_by: Actor
    received_by: Actor

@dataclass
class LastAggregate:
    name: str
    cardinality: Cardinality

class CaptureSheetParser:
    def __init__(self, rows: List[CaptureSheetRowModel]) -> None:
        self.rows = rows
        self.capture_sheet = CaptureSheetModel()
        self.last_event: LastEvent = None
        self.last_aggregate: LastAggregate = None
        self.property_buffer = list()
        self.aggregate_buffer = list()

    def parse_row_property(self, row: CaptureSheetRowModel):
        semantic_type = row.semantic_type
        if not self.capture_sheet.is_present(semantic_type, self.capture_sheet.semantic_types):
            self.capture_sheet.semantic_types[semantic_type] = SemanticType(name=semantic_type)

        property_attribute = row.attribute
        if not self.capture_sheet.is_present(
            property_attribute, self.capture_sheet.property_attributes
        ):
            self.capture_sheet.property_attributes[property_attribute] = PropertyAttribute(
                name=property_attribute,
                semantic_type=self.capture_sheet.semantic_types[semantic_type],
            )

        database = row.database
        if not self.capture_sheet.is_present(database, self.capture_sheet.databases):
            self.capture_sheet.databases[database] = Database(name=database)

        database_table = row.table
        if not self.capture_sheet.is_present(database_table, self.capture_sheet.database_tables):
            self.capture_sheet.database_tables[database_table] = DatabaseTable(
                name=database_table, database=self.capture_sheet.databases[database]
            )

        database_column = row.column
        if not self.capture_sheet.is_present(database_column, self.capture_sheet.database_columns):
            self.capture_sheet.database_columns[database_column] = DatabaseColumn(
                name=database_column,
                table=self.capture_sheet.database_tables[database_table],
                schema_type=row.schema_type,
                not_null=row.not_null,
                is_unique=row.is_unique,
                # TODO references
                references=None,
            )

        return self.new_property(property_attribute, database_column, row.attribute_cardinality)

    def new_property(self, property_attribute, database_column, attribute_cardinality):
        attribute = None
        source = None
        # TODO is_identifier
        is_identifier = False

        if property_attribute is not None:
            attribute = self.capture_sheet.property_attributes[property_attribute]
        if database_column is not None:
            source = self.capture_sheet.database_columns[database_column]

        return Property(
            name=self.capture_sheet.property_attributes[property_attribute].name,
            attribute=attribute,
            source=source,
            cardinality=attribute_cardinality,
            is_identifier=is_identifier,
        )
        
    def parse_row(self, row: CaptureSheetRowModel):        
        event_name = row.event
        aggregate_name = row.entity
        raised_by = row.raised_by
        received_by = row.received_by
        aggregate_cardinality = row.entity_cardinality

        if self.last_aggregate is not None and self.last_aggregate.name != aggregate_name:
            self.add_last_aggregate()

        if not self.capture_sheet.is_present(raised_by, self.capture_sheet.actors):
            self.capture_sheet.actors[raised_by] = Actor(name=raised_by)

        if not self.capture_sheet.is_present(received_by, self.capture_sheet.actors):
            self.capture_sheet.actors[received_by] = Actor(name=received_by)

        if self.last_event is not None and self.last_event.name != event_name:
            self.add_last_event()

        self.last_event = LastEvent(
            name = event_name,
            raised_by = self.capture_sheet.actors[raised_by],
            received_by = self.capture_sheet.actors[received_by],
        )

        self.last_aggregate = LastAggregate(
            name=aggregate_name,
            cardinality=aggregate_cardinality,
        )

        self.property_buffer.append(self.parse_row_property(row))

    def add_last_event(self):
        event_name = self.last_event.name
        raised_by = self.last_event.raised_by
        received_by = self.last_event.received_by

        new_event = Event(
                name=event_name,
                raised_by = raised_by,
                received_by = received_by,
                aggregates = self.aggregate_buffer,
            )

        self.capture_sheet.events[event_name] = new_event

        self.property_buffer = list()
        self.aggregate_buffer = list()

    def add_last_aggregate(self):
        aggregate_name = self.last_aggregate.name
        aggregate_cardinality = self.last_aggregate.cardinality

        new_aggregate = Aggregate(name=aggregate_name, properties=self.property_buffer)
        self.capture_sheet.aggregates[aggregate_name] = new_aggregate
        self.property_buffer = list()

        new_event_aggregate = EventAggregate(
                name=aggregate_name,
                aggregate=self.capture_sheet.aggregates[aggregate_name],
                cardinality=aggregate_cardinality,
            )

        self.aggregate_buffer.append(new_event_aggregate)
        
    def parse(self):
        for row in self.rows:
            self.parse_row(row)

        # be sure to get the last aggregate and event
        self.add_last_aggregate()
        self.add_last_event()

        return self.capture_sheet



def load_capture_sheet_rows(validation_path: Path, ignore_errors: bool = False):
    validation_data = json.loads(validation_path.read_text())
    error_rows = [x[RESULT] for x in validation_data if not x[OUTCOME]]

    if len(error_rows) > 0:
        if ignore_errors:
            print(
                f"WARNING: {len(error_rows)} rows failed validation and will be ignored."
            )
        else:
            raise Exception(f"{len(error_rows)} rows failed validation.")

    return [CaptureSheetRowModel(**x[RESULT]) for x in validation_data if x[OUTCOME]]


def parse_capture_sheet_rows(rows: List[CaptureSheetRowModel]):
    capture_sheet_parser = CaptureSheetParser(rows)
    capture_sheet_parser.parse()
    return capture_sheet_parser.capture_sheet

