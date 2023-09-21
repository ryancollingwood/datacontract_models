import pandas as pd
from common.str_utils import pascal_case
from .column_names import (
    ENTITY_CARDINALITY,
    ATTRIBUTE_CARDINALITY,
    EVENT,
    ATTRIBUTE,
    DATA_CLASSIFICATION,
)
from .column_ranges import column_subset
from .column_remapper import ColumnRemapper


def normalise_column_names(df: pd.DataFrame) -> pd.DataFrame:
    columns = list(df.columns)
    columns = [
        x.lower().strip().replace(" ", "_") if isinstance(x, str) else x
        for x in columns
    ]
    df.columns = columns
    return df


def pascal_case_column_values(df: pd.DataFrame, column: str) -> pd.DataFrame:
    has_values_ix = ~df[column].isnull()
    df.loc[has_values_ix, column] = df.loc[has_values_ix, column].apply(pascal_case)
    return df


def add_optional_columns(df: pd.DataFrame) -> pd.DataFrame:
    for col in [DATA_CLASSIFICATION]:
        if col not in df.columns:
            df[col] = None
    return df


def preprocess_capture_sheet(df: pd.DataFrame) -> pd.DataFrame:
    df = add_optional_columns(df)
    df = df.replace({"": None})

    df.pipe(normalise_column_names).pipe(
        pascal_case_column_values, ENTITY_CARDINALITY
    ).pipe(pascal_case_column_values, ATTRIBUTE_CARDINALITY).pipe(
        pascal_case_column_values, DATA_CLASSIFICATION
    )

    df_columns = ColumnRemapper(df.columns)
    df = df[df_columns.sorted_columns]

    for ffill_cols in [df_columns.event_columns, df_columns.entity_columns]:
        for col in ffill_cols:
            df[col] = df[col].ffill()

    return df
