import pandas as pd
from common.str_utils import pascal_case
from .column_names import ENTITY_CARDINALITY, ATTRIBUTE_CARDINALITY, EVENT, RAISED_BY, RECEIVED_BY, ENTITY

def normalise_column_names(df: pd.DataFrame) -> pd.DataFrame:
  columns = list(df.columns)
  columns = [x.lower().strip().replace(" ", "_") if isinstance(x, str) else x for x in columns]
  df.columns = columns
  return df

def pascal_case_column_values(df: pd.DataFrame, column: str) -> pd.DataFrame:
  has_values_ix = ~df[column].isnull()
  df.loc[has_values_ix, column] = df.loc[has_values_ix, column].apply(pascal_case)
  return df

def preprocess_capture_sheet(df: pd.DataFrame) -> pd.DataFrame:
  df = df.replace({"": None})
  df.pipe(normalise_column_names).\
    pipe(pascal_case_column_values, ENTITY_CARDINALITY).\
    pipe(pascal_case_column_values, ATTRIBUTE_CARDINALITY)

  for col in [
      EVENT, RAISED_BY, RECEIVED_BY,
      ENTITY, ENTITY_CARDINALITY]:
    df[col] = df[col].ffill()

  df = df.dropna(how="all", axis = 1)

  return df