from typing import Dict, List
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

from .models.capture_sheet_model import CaptureSheetModel
from .models.capture_sheet_row_model import CaptureSheetRowModel


def parse_row(capture_sheet: CaptureSheetModel, row: CaptureSheetRowModel):
    semantic_type = row.semantic_type
    if not capture_sheet.is_present(semantic_type, capture_sheet.semantic_types):
        capture_sheet.semantic_types[semantic_type] = SemanticType(name=semantic_type)

    property_attribute = row.attribute
    if not capture_sheet.is_present(
        property_attribute, capture_sheet.property_attributes
    ):
        capture_sheet.property_attributes[property_attribute] = PropertyAttribute(
            name=property_attribute,
            semantic_type=capture_sheet.semantic_types[semantic_type],
        )

    received_by = row.received_by
    if not capture_sheet.is_present(received_by, capture_sheet.actors):
        capture_sheet.actors[received_by] = Actor(name=received_by)

    database = row.database
    if not capture_sheet.is_present(database, capture_sheet.databases):
        capture_sheet.databases[database] = Database(name=database)

    database_table = row.table
    if not capture_sheet.is_present(database_table, capture_sheet.database_tables):
        capture_sheet.database_tables[database_table] = DatabaseTable(
            name=database_table, database=capture_sheet.databases[database]
        )

    database_column = row.column
    if not capture_sheet.is_present(database_column, capture_sheet.database_columns):
        capture_sheet.database_columns[database_column] = DatabaseColumn(
            name=database_column,
            table=capture_sheet.database_tables[database_table],
            not_null=row.not_null,
            is_unique=row.is_unique,
            # TODO references
            references=None,
        )


def parse_capture_sheet_rows(rows: List[CaptureSheetRowModel]):
    capture_sheet = CaptureSheetModel()

    for row in rows:
        parse_row(capture_sheet, row)

    return capture_sheet
