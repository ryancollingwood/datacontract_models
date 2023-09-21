from typing import Tuple
import pandas as pd

from .column_remapper import ColumnRemapper
from .preprocess import preprocess_capture_sheet
from .validate import validate_capture_sheet

def process_capture_sheet(df) -> Tuple[pd.DataFrame, pd.DataFrame, ColumnRemapper]:
    df, column_remapper = preprocess_capture_sheet(df)
    validation_df = validate_capture_sheet(df, column_remapper).reset_index()
    return df, validation_df, column_remapper