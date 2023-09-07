import pandas as pd
from .preprocess import preprocess_capture_sheet
from .validate import validate_capture_sheet

def process_capture_sheet(df):
    df = preprocess_capture_sheet(df)
    validation_df = validate_capture_sheet(df).reset_index()
    return df, validation_df