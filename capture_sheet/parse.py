from pathlib import Path
from typing import List
import json
from models import (
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
from models import Actor

from .models.capture_sheet_model import CaptureSheetModel
from .models.capture_sheet_row_model import CaptureSheetRowModel
from .column_names import RESULT, OUTCOME
from .column_remapper import ColumnRemapper
from .models.parse_models import LastEvent, LastAggregate
from .file_names import COLUMN_REMAPPER_JSON

class CaptureSheetParser:
    def __init__(self, rows: List[CaptureSheetRowModel], column_remapper: ColumnRemapper) -> None:
        self.rows = rows
        self.column_remapper = column_remapper
        self.capture_sheet = CaptureSheetModel()
        self.last_event: LastEvent = None
        self.last_aggregate: LastAggregate = None
        self.property_buffer = list()
        self.aggregate_buffer = list()

    def parse_row_property(self, row: CaptureSheetRowModel):
        semantic_type = row.semantic_type
        if not self.capture_sheet.is_present(semantic_type, self.capture_sheet.semantic_types):
            self.capture_sheet.semantic_types[semantic_type] = SemanticType(
                name=semantic_type,
                classification=row.data_classification,
                )

        property_attribute = row.attribute
        if not self.capture_sheet.is_present(
            property_attribute, self.capture_sheet.property_attributes
        ):
            attribute_extra = {k:v for k,v in row.model_extra.items() if k in self.column_remapper.attribute_columns}
            self.capture_sheet.property_attributes[property_attribute] = PropertyAttribute(
                name=property_attribute,
                semantic_type=self.capture_sheet.semantic_types[semantic_type],
                **attribute_extra,
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

        return self.new_property(row, property_attribute, database_column, row.attribute_cardinality)

    def new_property(self, row, property_attribute, database_column, attribute_cardinality):
        attribute = None
        source = None
        # TODO is_identifier
        is_identifier = False

        if property_attribute is not None:
            attribute = self.capture_sheet.property_attributes[property_attribute]
        if database_column is not None:
            source = self.capture_sheet.database_columns[database_column]

        property_extra = {k:v for k,v in row.model_extra.items() if k in self.column_remapper.property_columns}
        return Property(
            attribute=attribute,
            source=source,
            cardinality=attribute_cardinality,
            is_identifier=is_identifier,
            **property_extra,
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

        event_extra = {k:v for k,v in row.model_extra.items() if k in self.column_remapper.event_columns}

        self.last_event = LastEvent(
            name = event_name,
            raised_by = self.capture_sheet.actors[raised_by],
            received_by = self.capture_sheet.actors[received_by],
            **event_extra
        )

        aggregate_extra = {k:v for k,v in row.model_extra.items() if k in self.column_remapper.entity_columns}

        self.last_aggregate = LastAggregate(
            name=aggregate_name,
            cardinality=aggregate_cardinality,
            **aggregate_extra
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
                **self.last_event.model_extra,
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


