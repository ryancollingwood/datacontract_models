from typing import List
import pandas as pd
from .column_names import EVENT, RAISED_BY, RECEIVED_BY
from .column_names import ENTITY, ENTITY_CARDINALITY
from .column_names import ATTRIBUTE, ATTRIBUTE_CARDINALITY
from .column_names import SEMANTIC_TYPE, DATA_CLASSIFICATION
from .column_names import SCHEMA_TYPE, DATABASE, TABLE, COLUMN, NOT_NULL, IS_UNIQUE
from .column_names import REFERENCE_DATABASE, REFERENCE_TABLE, REFERENCE_COLUMN

EVENT_COLUMNS = (EVENT, RAISED_BY, RECEIVED_BY,)
ENTITY_COLUMNS = (ENTITY, ENTITY_CARDINALITY,)
PROPERTY_COLUMNS = (ATTRIBUTE,ATTRIBUTE_CARDINALITY,)
ATTRIBUTE_COLUMNS = (SEMANTIC_TYPE, DATA_CLASSIFICATION,)
SOURCE_COLUMNS = (SCHEMA_TYPE, DATABASE, TABLE, COLUMN, NOT_NULL, IS_UNIQUE,)
REFERENCE_COLUMNS = (REFERENCE_DATABASE, REFERENCE_TABLE, REFERENCE_COLUMN,)

EVENT_PREFIX = "event_"
ENTITY_PREFIX = "entity_"
PROPERTY_PREFIX = "property_"
ATTRIBUTE_PREFIX = "attribute_"
SOURCE_PREFIX = "source_"
REFERENCE_PREFIX = "reference_"

COLUMN_MAP = {
    EVENT_PREFIX: EVENT_COLUMNS,
    ENTITY_PREFIX: ENTITY_COLUMNS,
    PROPERTY_PREFIX: PROPERTY_COLUMNS,
    ATTRIBUTE_PREFIX: ATTRIBUTE_COLUMNS,
    SOURCE_PREFIX: SOURCE_COLUMNS,
    REFERENCE_PREFIX: REFERENCE_COLUMNS,
}


def column_subset(df: pd.DataFrame, start_col_name: str, end_col_name: str, end_is_inclusive: bool = True):
    columns: List[str] = list(df.columns)
    start_index = columns.index(start_col_name)
    end_index = columns.index(end_col_name) + 1 if end_is_inclusive else columns.index(end_col_name)

    if start_index == end_index:
        return ValueError("Cannot get a column subset, columns have same index")
    if end_index < start_index:
        return ValueError("End column name is before start column name")
    
    return columns[start_index:end_index]

def resort_columns(df_columns: List[str]) -> List[str]:
    """
    Get the order of columns sorted so that they are in the order of:
    Event, Entity, Property, Attribute, Source, Reference. While keeping 
    any additional columns with the same prefix in the same order
    """
    result = list()

    for prefix, column_range in COLUMN_MAP.items():
        additional_prefix_columns = [column for column in df_columns if column.startswith(prefix) and column not in column_range]
        additional_prefix_columns = [x for x in additional_prefix_columns if x not in result]

        for i, column in enumerate(column_range):
            if column not in df_columns:
                raise ValueError(f"Column {column} not found in dataframe")
            
            result.append(column)

            if i == 0 and len(additional_prefix_columns) > 0:
                result.extend(additional_prefix_columns)
            
    if len(result) != len(df_columns):
        difference = [x for x in df_columns if x not in result]
        raise ValueError(f"Not all columns were sorted: {difference}")
    
    return result
