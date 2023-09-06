import pandas as pd
from .preprocess import preprocess_capture_sheet
from .validate import validate_capture_sheet

def process_capture_sheet(df):
    df = preprocess_capture_sheet(df)
    validation_df = validate_capture_sheet(df)
    failed_validated_df = validation_df.loc[validation_df["outcome"] == False, :]
    if len(failed_validated_df) > 0:
        print(failed_validated_df.head())
    return df, validation_df