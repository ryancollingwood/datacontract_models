from typing import List
import pandas as pd
from common.str_utils import pascal_case
from .column_names import (
    ENTITY_CARDINALITY,
    ATTRIBUTE_CARDINALITY,
    DATA_CLASSIFICATION,
)


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


def add_optional_columns(df: pd.DataFrame, optional_columns: List[str]) -> pd.DataFrame:
    """
    Add optional columns to the dataframe if they don't already exist
    """
    for col in optional_columns:
        if col not in df.columns:
            df[col] = None
    return df


def preprocess_columns(
    df: pd.DataFrame, optional_columns: List[str] = None
) -> pd.DataFrame:
    result_df = df.copy()

    if optional_columns is not None:
        result_df = add_optional_columns(result_df, optional_columns)
    result_df = result_df.replace({"": None})

    result_df.pipe(normalise_column_names).pipe(
        pascal_case_column_values, ENTITY_CARDINALITY
    ).pipe(pascal_case_column_values, ATTRIBUTE_CARDINALITY).pipe(
        pascal_case_column_values, DATA_CLASSIFICATION
    )

    return result_df


def ffill_sparse_cols(df, column_groups: List[List[str]]):
    for ffill_cols in column_groups:
        for col in ffill_cols:
            df[col] = df[col].ffill()
    return df

