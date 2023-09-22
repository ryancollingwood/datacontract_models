from typing import List
from copy import deepcopy
import json
import pandas as pd
from pydantic import ValidationError
from .models.capture_sheet_row_model import CaptureSheetRowModel
from .column_names import OUTCOME, RESULT

def validate_df_row(row):
    try:
        # remove np.nan values as it trips up pydantic
        values = {k:v for k,v in row.to_dict().items() if not pd.isnull(v)}
        result = CaptureSheetRowModel(**values)
        return True, result
    except ValidationError as e:
        return False, e


def validate_capture_sheet_model(df: pd.DataFrame) -> pd.DataFrame:
    result_df = pd.DataFrame(
        [validate_df_row(df.iloc[x]) for x in range(len(df))],
        columns=[OUTCOME, RESULT],
    )

    # having to double handle the json conversion is a bit of a hack
    # so that we can get the json representation of the pydantic model
    # or the exception if one was raised
    result_df[RESULT] = result_df[RESULT].apply(lambda x: json.loads(x.json()))
    return result_df


def check_uniqueness(
    df: pd.DataFrame,
    check_column: str,
    partition_cols: List[str] = None,
    parent_cols: List[str] = None,
):
    """
    Check that the values in the `check_column` are unique for the given
    partition and parent columns.

    Args:
        df (pd.DataFrame)
        check_column (str): Column to check for unique values
        partition_cols (List[str], optional): The subset of columns to be 
            evaluated as part of the uniqueness check.
            Defaults to None.
        parent_cols (List[str], optional): The column by which we want to
            groupby after having filtered to subset of columns.
            Defaults to None.

    Raises:
        e: AssertionError if the uniqueness check fails
    """
    if partition_cols is not None:
        actual_partition = deepcopy(partition_cols)
        if not isinstance(actual_partition, list):
            actual_partition = list(actual_partition)
        if check_column not in actual_partition:
            actual_partition.append(check_column)
    else:
        actual_partition = None

    select_cols = [check_column]
    if partition_cols is not None:
        select_cols += [x for x in partition_cols if x not in select_cols]
    if parent_cols is not None:
        select_cols += [x for x in parent_cols if x not in select_cols]

    select_cols = list(set(select_cols))

    check_df = df[select_cols].copy()

    if actual_partition is not None:
        check_df = check_df.drop_duplicates(subset=actual_partition, keep="first")
        if parent_cols is None:
            check_counts = check_df[check_column].value_counts()
        else:
            check_counts = check_df.groupby(parent_cols)[check_column].value_counts()
    else:
        check_counts = check_df[check_column].value_counts()

    try:
        msg = f"for column `{check_column}`"
        if partition_cols is not None:
            msg = f"{msg} for partition ({actual_partition})"
        msg = f"Uniqueness check failed: {msg}"
        assert max(check_counts) == 1, msg
    except AssertionError as e:
        raise e
